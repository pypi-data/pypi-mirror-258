from __future__ import annotations
from contextlib import nullcontext
from datetime import date, datetime, time
from decimal import Decimal
from io import IOBase
import logging
import os
from pathlib import Path
import re
from urllib.parse import urlparse
from typing import TypeVar
from uuid import UUID
from secrets import token_hex

from ..text import build_url, skip_utf8_bom
from ..format import Format
from ..choices import _registered_choices_tables
from ..types import Literal
from .base import ColumnInfo, DbAdapter, T_Connection, T_Cursor, T_Composable, T_Composed

logger = logging.getLogger(__name__)

# psycopg v3
try:
    from psycopg import Connection as v3_Connection, Cursor as v3_Cursor, sql as v3_sql, connect as v3_connect
    from psycopg.errors import Diagnostic
    v3_Composable = v3_sql.Composable
    v3_Composed = v3_sql.Composed
except ImportError:
    v3_Connection = type(None)
    v3_Cursor = type(None)
    v3_Composable = type(None)
    v3_Composed = type(None)
    v3_sql = None

# psycopg v2
try:
    from psycopg2 import sql as v2_sql, connect as v2_connect
    from psycopg2.extensions import connection as v2_Connection, cursor as v2_Cursor
    v2_Composable = v2_sql.Composable
    v2_Composed = v2_sql.Composed
except:
    v2_Connection = type(None)
    v2_Cursor = type(None)
    v2_Composable = type(None)
    v2_Composed = type(None)
    v2_sql = None


class PgBaseAdapter(DbAdapter[T_Connection, T_Cursor, T_Composable, T_Composed]):
    URL_SCHEME = 'postgresql' # See: https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
    DEFAULT_SCHEMA = 'public'
    _sql = v3_sql
    

    @classmethod
    def is_available(cls):
        return cls._sql is not None
   

    # -------------------------------------------------------------------------
    # Execute utils
    #
    
    def execute_procedure(self, name: str|tuple, *args) -> T_Cursor:
        schema, name = self.split_name(name)
        
        query = "CALL "
        params = []
            
        if schema:    
            query +="{}."
            params += [self.escape_identifier(schema)]

        query += "{}"
        params += [self.escape_identifier(name)]

        query += "(" + ", ".join(['{}'] * len(args)) + ")"
        params += [self.get_composable_param(arg) for arg in args]

        with self.cursor() as cursor:
            with self.register_notice_handler(if_exists=None, logprefix=f"pg:{schema + '.' if schema and schema != self.DEFAULT_SCHEMA else ''}{name}"):
                cursor.execute(self._sql.SQL(query).format(*params))
                return cursor
            

    def register_notice_handler(self, if_exists = '__raise__', logprefix = 'pg'):
        """
        Usage example with Django:

        ```
        from django.apps import AppConfig
        from django.db.backends.signals import connection_created
        from zut import PgAdapter # or 'Pg2Adapter' for psycopg2

        class MyDjangoProjectConfig(AppConfig):
            default_auto_field = 'django.db.models.BigAutoField'
            name = 'mydjangiproject'
            
            def ready(self):
                connection_created.connect(connection_created_receiver)

        def connection_created_receiver(sender, connection, **kwargs):
            if connection.alias == "default":
                Pg2Adapter(connection).register_notice_handler()
        ```
        """
        raise NotImplementedError() # implemented in concrete subclasses


    # -------------------------------------------------------------------------
    # Queries
    #
    
    def get_select_table_query(self, table: str|tuple, schema_only = False) -> PgAdapter._sql.Composed:
        schema, table = self.split_name(table)

        query = "SELECT * FROM "
        params = []
            
        if schema:    
            query +="{}."
            params += [self.escape_identifier(schema)]

        query += "{}"
        params += [self.escape_identifier(table)]
        
        if schema_only:
            query += ' WHERE false'

        return self._sql.SQL(query).format(*params)


    def get_composable_param(self, value):
        if value is None:
            return self._sql.SQL("null")
        elif value == '__now__':
            return self._sql.SQL("NOW()")
        elif isinstance(value, self._sql.Composable):
            return value
        else:
            return self.escape_literal(value)
        

    def escape_identifier(self, value) -> PgAdapter._sql.Composable:
        return self._sql.Identifier(value)
    

    def escape_literal(self, value) -> PgAdapter._sql.Composable:
        return self._sql.Literal(value)
    

    # -------------------------------------------------------------------------
    # region Schemas, tables and columns
    #    

    def schema_exists(self, schema: str) -> bool:
        query = "SELECT EXISTS (SELECT FROM pg_namespace WHERE nspname = %s)"
        params = [schema]

        return self.get_scalar(query, params)
    

    def create_schema(self, schema: str):
        query = "CREATE SCHEMA {}"
        params = [self._sql.Identifier(schema)]

        return self.execute_query(self._sql.SQL(query).format(*params))
    

    def drop_schema(self, schema: str, cascade: bool = False):
        query = "DROP SCHEMA {}"
        params = [self._sql.Identifier(schema)]

        if cascade:
            query += " CASCADE"

        return self.execute_query(self._sql.SQL(query).format(*params))
    

    def table_exists(self, table: str|tuple) -> bool:
        schema, table = self.split_name(table)

        query = "SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = %s AND tablename = %s)"
        params = [schema, table]

        return self.get_scalar(query, params)
    

    def drop_table(self, table: str|tuple):
        schema, table = self.split_name(table)
        
        query = "DROP TABLE "
        params = []
            
        if schema:    
            query +="{}."
            params += [self.escape_identifier(schema)]

        query += "{}"
        params += [self.escape_identifier(table)]

        self.execute_query(self._sql.SQL(query).format(*params))
        

    def truncate_table(self, table: str|tuple, cascade: bool = False):
        schema, table = self.split_name(table)
        
        query = "TRUNCATE "
        params = []
            
        if schema:    
            query +="{}."
            params += [self.escape_identifier(schema)]

        query += "{}"
        params += [self.escape_identifier(table)]

        if cascade:
            query += " CASCADE"

        self.execute_query(self._sql.SQL(query).format(*params))


    def _update_column_info(self, info: ColumnInfo, cursor: T_Cursor, index: int):
        info.name, type_oid, display_size, internal_size, precision, scale, always_none = cursor.description[index]
        type_info = OID_CATALOG.get(type_oid)
        if type_info:
            info.sql_type, info.python_type = type_info
        else:
            info.sql_type = type_oid
    
    # endregion
            

    def load_from_csv(self, file: os.PathLike|IOBase, table: str|tuple, columns: list[str] = None, encoding: str = 'utf-8', *, merge: Literal['truncate', 'truncate-cascade', 'upsert'] = None, noheaders: bool = False, delimiter: str = None, quotechar: str = None, nullval: str = None) -> int:
        sche, tab = self.split_name(table)
        tmp_tab: str = None
        key_columns: list[str] = []
        nonkey_target_columns: list[str] = []
        
        delimiter, quotechar, nullval = Format.apply_csv_defaults(delimiter, quotechar, nullval)

        try:
            if merge in ['truncate', 'truncate-cascade']:                
                self.truncate_table((sche, tab), cascade=merge == 'truncate-cascade')

            elif merge == 'upsert':
                with self.cursor() as cursor:
                    # Retrieve information about the columns
                    sql = """
                    WITH pk_columns AS (
                        SELECT c.column_name
                        FROM information_schema.table_constraints tc 
                        LEFT OUTER JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name) 
                        LEFT OUTER JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema AND tc.table_name = c.table_name AND ccu.column_name = c.column_name
                        WHERE tc.constraint_type = 'PRIMARY KEY' AND tc.constraint_schema = %(schema)s and tc.table_name = %(table)s
                    )
                    SELECT
                        c.ordinal_position AS position
                        ,c.column_name AS name
                        ,c.udt_name AS sql_type
                        ,c.is_nullable = 'YES' AS is_nullable
                        ,p.column_name IS NOT NULL AS is_primary_key
                    FROM information_schema.columns c
                    LEFT OUTER JOIN pk_columns p ON p.column_name = c.column_name
                    WHERE table_schema = %(schema)s AND table_name = %(table)s
                    """
                    logger.debug("retrieve %s.%s columns", sche, tab)
                    target_colinfos = self.execute_query(sql, {'schema': sche, 'table': tab}, cursor=cursor, results=True)

                    # Build a temporary table
                    tmp_tab = f"tmp_{tab}_{token_hex(4)}"
                    params = []                
                    sql = "CREATE TEMPORARY TABLE {} ("; params += [self._sql.Identifier(tmp_tab)]
                    pk = []
                    target_colnames = set()

                    for i, colinfo in enumerate(target_colinfos):
                        name = colinfo['name']
                        
                        is_primary_key = colinfo['is_primary_key']
                        if columns and not name in columns:
                            if is_primary_key:
                                raise ValueError(f"primary key column '{name}' must be included in the list of copied columns")
                            continue

                        sql += ("," if i > 0 else " ") + "{} {} {}"; params += [self._sql.Identifier(name), self._sql.Identifier(colinfo['sql_type']), self._sql.SQL('NULL' if colinfo['is_nullable'] else 'NOT NULL')]
                        target_colnames.add(name)
                        if is_primary_key:
                            pk.append(name)
                            key_columns.append(name)
                        else:
                            nonkey_target_columns.append(name)

                    # additional columns if any ('COPY FROM' cannot discard some columns so we have to import them anyway)
                    if columns:
                        for name in columns:
                            if not name in target_colnames:
                                sql += ',{} text NULL'; params += [self._sql.Identifier(name)]
                    
                    if pk:
                        sql += ", PRIMARY KEY ("
                        for i, name in enumerate(pk):
                            sql += (", " if i > 0 else " ") + "{}"; params += [self._sql.Identifier(name)]
                        sql += ")"
                    
                    sql += ")"
                    
                    if logger.isEnabledFor(logging.DEBUG):
                        logger.debug("columns (for COPY operation): %s", columns)
                        logger.debug("key_columns: %s", key_columns)
                        logger.debug("nonkey_target_columns: %s", nonkey_target_columns)

                    logger.debug("create temp table %s", tmp_tab)
                    self.execute_query(self._sql.SQL(sql).format(*params), cursor=cursor)

            # Prepare actual copy operation
            sql = "COPY "; params = []
                
            if tmp_tab:
                sql += "{}"; params += [self.escape_identifier(tmp_tab)]
            else:    
                if sche:    
                    sql +="{}."; params += [self.escape_identifier(sche)]
                sql += "{}"; params += [self.escape_identifier(tab)]

            if columns:
                sql += " ("
                for i, colinfo in enumerate(columns):
                    sql += (", " if i > 0 else "") + "{}"; params += [self.escape_identifier(colinfo)]
                sql += ")"

            sql += " FROM STDIN (FORMAT csv"
            sql += ', ENCODING {}'; params.append('utf-8' if encoding == 'utf-8-sig' else self.escape_literal(encoding))
            sql += ', DELIMITER {}'; params.append(self.escape_literal(delimiter))
            sql += ', QUOTE {}'; params.append(self.escape_literal(quotechar))            
            sql += ', ESCAPE {}'; params.append(self.escape_literal(quotechar))
            sql += ', NULL {}'; params.append(self.escape_literal(nullval))
            if not noheaders:
                sql += ", HEADER match"
            sql += ")"

            with nullcontext(file) if isinstance(file, IOBase) else open(file, "rb") as fp:
                skip_utf8_bom(fp)
                if tmp_tab:
                    logger.debug("actual copy from %s to %s", file, tmp_tab)
                result_count = self._actual_copy(self._sql.SQL(sql).format(*params), fp)
            
            # Upsert from tmp table if necessary
            if tmp_tab:
                params = []
                sql = "INSERT INTO {}.{} ("; params += [self._sql.Identifier(sche), self._sql.Identifier(tab)]
                for i, colinfo in enumerate([*key_columns, *nonkey_target_columns]):
                    sql += ("," if i > 0 else "") + "{}"; params += [self._sql.Identifier(colinfo)]
                sql += ") SELECT "
                for i, colinfo in enumerate([*key_columns, *nonkey_target_columns]):
                    sql += ("," if i > 0 else "") + "{}"; params += [self._sql.Identifier(colinfo)]
                sql += " FROM {}"; params += [self._sql.Identifier(tmp_tab)]
                sql += " ON CONFLICT ("
                for i, colinfo in enumerate(key_columns):
                    sql += ("," if i > 0 else "") + "{}"; params += [self._sql.Identifier(colinfo)]
                sql += ") DO UPDATE SET "
                for i, colinfo in enumerate(nonkey_target_columns):
                    sql += ("," if i > 0 else "") + "{}=EXCLUDED.{}"; params += [self._sql.Identifier(colinfo), self._sql.Identifier(colinfo)]
                
                logger.debug("upsert from %s to %s.%s", tmp_tab, sche, tab)
                self.execute_query(self._sql.SQL(sql).format(*params))

            return result_count

        finally:
            if tmp_tab:
                self.execute_query(self._sql.SQL("DROP TABLE IF EXISTS {}").format(self._sql.Identifier(tmp_tab)))


    # -------------------------------------------------------------------------
    # region Reinit (Django command)
    #    

    def move_all_to_new_schema(self, new_schema: str, old_schema: str = "public"):
        query = """DO LANGUAGE plpgsql $$
    DECLARE
        old_schema name = {old_schema};
        new_schema name = {new_schema};
        sql_query text;
    BEGIN
        -- Create schema
        sql_query = format('CREATE SCHEMA %I', new_schema);
        RAISE NOTICE 'applying %', sql_query;
        EXECUTE sql_query;
    
        -- Move tables and views
        FOR sql_query IN
            SELECT
                format('ALTER %s %I.%I SET SCHEMA %I', CASE WHEN table_type IN ('BASE TABLE') THEN 'TABLE' ELSE table_type END, table_schema, table_name, new_schema)
            FROM information_schema.tables
            WHERE table_schema = old_schema
            AND table_name NOT IN ('geography_columns', 'geometry_columns', 'spatial_ref_sys') -- postgis
        LOOP
            RAISE NOTICE 'applying %', sql_query;
            EXECUTE sql_query;
        END LOOP;
    
        -- Move routines
        FOR sql_query IN
            SELECT
                format('ALTER %s %I.%I%s SET SCHEMA %I', routine_type, routine_schema, routine_name, routine_params, new_schema)
            FROM (
                SELECT
                    specific_name, routine_type, routine_schema, routine_name
                    ,CASE WHEN routine_params IS NULL THEN '()' ELSE CONCAT('(',  routine_params, ')') END AS routine_params
                FROM (
                    SELECT
                        r.specific_name
                        ,r.routine_type, r.routine_schema, r.routine_name
                        ,string_agg(p.data_type, ', ' order by p.ordinal_position ) AS routine_params
                    FROM information_schema.routines r
                    LEFT OUTER JOIN information_schema.parameters p ON p.specific_name = r.specific_name
                    GROUP BY
                        r.specific_name
                        ,r.routine_type, r.routine_schema, r.routine_name
                ) s
            ) s
            WHERE routine_schema = old_schema
            -- postgis:
            AND routine_name NOT LIKE 'box%%'
            AND routine_name NOT LIKE '%%geography%%' AND routine_name NOT LIKE 'geog_%%'
            AND routine_name NOT LIKE '%%geometry%%' AND routine_name NOT LIKE 'geom%%'
            AND routine_name NOT LIKE 'gidx_%%'
            AND routine_name NOT LIKE 'gserialized_%%'
            AND routine_name NOT LIKE 'overlaps_%%'
            AND routine_name NOT LIKE 'postgis_%%' AND routine_name NOT LIKE '_postgis_%%' AND routine_name NOT LIKE 'pgis_%%'
            AND routine_name NOT LIKE 'spheroid_%%'
            AND routine_name NOT LIKE 'st_%%' AND routine_name NOT LIKE '_st_%%'
            AND routine_name NOT IN ('addauth', 'bytea', 'checkauth', 'checkauthtrigger', 'contains_2d', 'disablelongtransactions', 'enablelongtransactions', 'equals', 'find_srid', 'get_proj4_from_srid', 'gettransactionid', 'is_contained_2d', 'json', 'jsonb', 'lockrow', 'longtransactionsenabled', 'path', 'point', 'polygon', 'text', 'unlockrows')
            -- unaccent:
            AND routine_name NOT LIKE 'unaccent%%'
        LOOP
            RAISE NOTICE 'applying %', sql_query;
            EXECUTE sql_query;
        END LOOP;
    END; $$
    """
        params = {
            'old_schema': self.escape_literal(old_schema),
            'new_schema': self.escape_literal(new_schema if new_schema else "public"),
        }

        with self.cursor() as cursor:
            with self.register_notice_handler(if_exists=None, logprefix=f"pg:move_all_to_new_schema"):
                cursor.execute(self._sql.SQL(query).format(**params))


    def drop_all(self, schema: str = "public"):
        query = """DO LANGUAGE plpgsql $$
    DECLARE
        old_schema name = {old_schema};
        sql_query text;
    BEGIN
        -- Remove foreign-key constraints
        FOR sql_query IN
            SELECT
                format('ALTER TABLE %I.%I DROP CONSTRAINT %I', table_schema, table_name, constraint_name)
            FROM information_schema.table_constraints
            WHERE table_schema = old_schema AND constraint_type = 'FOREIGN KEY'
            AND table_name NOT IN ('geography_columns', 'geometry_columns', 'spatial_ref_sys') -- postgis
        LOOP
            RAISE NOTICE 'applying %', sql_query;
            EXECUTE sql_query;
        END LOOP;

        -- Drop tables and views
        FOR sql_query IN
            SELECT
                format('DROP %s IF EXISTS %I.%I CASCADE', CASE WHEN table_type IN ('BASE TABLE') THEN 'TABLE' ELSE table_type END, table_schema, table_name)
            FROM information_schema.tables
            WHERE table_schema = old_schema
            AND table_name NOT IN ('geography_columns', 'geometry_columns', 'spatial_ref_sys') -- postgis
        LOOP
            RAISE NOTICE 'applying %', sql_query;
            EXECUTE sql_query;
        END LOOP;
    
        -- Drop routines
        FOR sql_query IN
            SELECT
                format('DROP %s IF EXISTS %I.%I%s CASCADE', routine_type, routine_schema, routine_name, routine_params)
            FROM (
                SELECT
                    specific_name, routine_type, routine_schema, routine_name
                    ,CASE WHEN routine_params IS NULL THEN '()' ELSE CONCAT('(',  routine_params, ')') END AS routine_params
                FROM (
                    SELECT
                        r.specific_name
                        ,r.routine_type, r.routine_schema, r.routine_name
                        ,string_agg(p.data_type, ', ' order by p.ordinal_position ) AS routine_params
                    FROM information_schema.routines r
                    LEFT OUTER JOIN information_schema.parameters p ON p.specific_name = r.specific_name
                    GROUP BY
                        r.specific_name
                        ,r.routine_type, r.routine_schema, r.routine_name
                ) s
            ) s
            WHERE routine_schema = old_schema
            -- postgis:
            AND routine_name NOT LIKE 'box%%'
            AND routine_name NOT LIKE '%%geography%%' AND routine_name NOT LIKE 'geog_%%'
            AND routine_name NOT LIKE '%%geometry%%' AND routine_name NOT LIKE 'geom%%'
            AND routine_name NOT LIKE 'gidx_%%'
            AND routine_name NOT LIKE 'gserialized_%%'
            AND routine_name NOT LIKE 'overlaps_%%'
            AND routine_name NOT LIKE 'postgis_%%' AND routine_name NOT LIKE '_postgis_%%' AND routine_name NOT LIKE 'pgis_%%'
            AND routine_name NOT LIKE 'spheroid_%%'
            AND routine_name NOT LIKE 'st_%%' AND routine_name NOT LIKE '_st_%%'
            AND routine_name NOT IN ('addauth', 'bytea', 'checkauth', 'checkauthtrigger', 'contains_2d', 'disablelongtransactions', 'enablelongtransactions', 'equals', 'find_srid', 'get_proj4_from_srid', 'gettransactionid', 'is_contained_2d', 'json', 'jsonb', 'lockrow', 'longtransactionsenabled', 'path', 'point', 'polygon', 'text', 'unlockrows')
            -- unaccent:
            AND routine_name NOT LIKE 'unaccent%%'
        LOOP
            RAISE NOTICE 'applying %', sql_query;
            EXECUTE sql_query;
        END LOOP;
    END; $$
    """
        params = {
            'old_schema': self.escape_literal(schema)
        }

        with self.cursor() as cursor:
            with self.register_notice_handler(if_exists=None, logprefix=f"pg:drop_all"):
                cursor.execute(self._sql.SQL(query).format(**params))
    

    # endregion

    def deploy_choices_table(self):
        with self.cursor() as cursor:
            for app_label, cls_list in _registered_choices_tables.items():
                for cls in cls_list:
                    db_table = cls.__name__.lower()
                    if app_label:
                        db_table = f'{app_label}_{db_table}'

                    logger.debug("deploy choices table %s", db_table)

                    # Create table if not exists
                    max_value_typebase = 1
                    for member in cls:
                        if issubclass(cls, int):
                            value_typebase = member.value
                        else:
                            value_typebase = len(member.value)
                        if value_typebase > max_value_typebase:
                            max_value_typebase = value_typebase

                    if issubclass(cls, int):
                        choices_value_type = 'smallint' if max_value_typebase <= 32767 else 'bigint'
                    else:
                        choices_value_type = f'char({max_value_typebase})'

                    query = "CREATE TABLE IF NOT EXISTS {choices_table} ("
                    query += "\n    id {choices_value_type} NOT NULL PRIMARY KEY"
                    query += "\n    ,name text NOT NULL UNIQUE"
                    query += "\n    ,label text NOT NULL UNIQUE"
                    query += "\n    ,created timestamptz NOT NULL DEFAULT now()"
                    query += "\n    ,updated timestamptz NOT NULL DEFAULT now()"
                    query += ");"

                    cursor.execute(self._sql.SQL(query).format(
                        choices_table = self.escape_identifier(db_table),
                        choices_value_type = self._sql.SQL(choices_value_type),
                    ))

                    # Upsert members
                    query = "INSERT INTO {} AS d (id, name, label, created, updated)"
                    params = [self.escape_identifier(db_table)]
                    query += "\nVALUES"
                    for i, member in enumerate(cls):
                        query += "\n    %s({}, {}, {}, now(), now())" % (',' if i > 0 else '')
                        params += [self.escape_literal(member.value), self.escape_literal(member.name), self.escape_literal(member.label)]
                    query += "\nON CONFLICT (id) DO UPDATE SET"
                    query += "\n    name = excluded.name"
                    query += "\n    ,label = excluded.label"
                    query += "\n    ,updated = CASE WHEN d.name != excluded.name OR d.label != excluded.label THEN now() ELSE d.updated END"
                    query += "\n;"

                    cursor.execute(self._sql.SQL(query).format(*params))


class PgAdapter(PgBaseAdapter[v3_Connection, v3_Cursor, v3_Composable, v3_Composed]):
    EXPECTED_CONNECTION_TYPES = ['psycopg.Connection']
    _sql = v3_sql

    def _create_connection(self) -> T_Connection:
        conn = v3_connect(self._connection_url, autocommit=self.autocommit)
        return conn
    
    
    def _get_url_from_connection(self):
        with self.cursor() as cursor:
            cursor.execute("SELECT session_user, inet_server_addr(), inet_server_port(), current_database()")
            user, host, port, dbname = next(iter(cursor))
        return build_url(scheme=self.URL_SCHEME, username=user, hostname=host, port=port, path='/'+dbname)


    def _actual_copy(self, query, fp):
        BUFFER_SIZE = 65536

        with self.cursor() as cursor:
            with cursor.copy(query) as copy:
                while True:
                    data = fp.read(BUFFER_SIZE)
                    if not data:
                        break
                    copy.write(data)
            return cursor.rowcount


    def register_notice_handler(self, logprefix = None, if_exists = '__raise__'):
        if self.connection._notice_handlers:
            if if_exists != '__raise__':
                return nullcontext(if_exists)
            raise ValueError(f"notice handler already registered: {self.connection._notice_handlers}")

        return PgNoticeManager(self.connection, logprefix)


class Pg2Adapter(PgBaseAdapter[v2_Connection, v2_Cursor, v2_Composable, v3_Composed]):
    EXPECTED_CONNECTION_TYPES = ['psycopg2.extensions.connection']
    _sql = v2_sql

    def _create_connection(self) -> T_Connection:
        kwargs = {}
        
        r = urlparse(self._connection_url)

        if r.hostname:
            kwargs['host'] = r.hostname
        if r.port:
            kwargs['port'] = r.port

        name = r.path.lstrip('/')
        if name:
            kwargs['dbname'] = name

        if r.username:
            kwargs['user'] = r.username
        if r.password:
            kwargs['password'] = r.password

        conn = v2_connect(**kwargs)
        conn.autocommit = self.autocommit
        return conn
    

    def _get_url_from_connection(self):    
        params = self.connection.get_dsn_parameters()
        return build_url(
            scheme=self.URL_SCHEME,
            path='/' + params.get('dbname', None),
            hostname=params.get('host', None),
            port=params.get('port', None),
            username=params.get('user', None),
            password=params.get('password', None),
        )
    

    def _actual_copy(self, query, fp):
        with self.cursor() as cursor:
            cursor.copy_expert(query, fp)
            return cursor.rowcount
    

    def register_notice_handler(self, logprefix = None, if_exists = '__raise__'):
        if self.connection.notices:
            if if_exists != '__raise__':
                return nullcontext(if_exists)
            raise ValueError(f"notice handler already registered: {self.connection.notices}")

        return Pg2NoticeHandler(self.connection, logprefix)

class PgNoticeManager:
    """
    This class can be used as a context manager that remove the handler on exit.

    The actual handler required by psycopg 3 `connection.add_notice_handler()` is the `pg_notice_handler` method.
    """
    def __init__(self, connection, logprefix: str = None):
        self.connection = connection
        self.logger = logging.getLogger(logprefix) if logprefix else None
        self.connection.add_notice_handler(self.handler)

    def __enter__(self):
        return self.handler
    
    def __exit__(self, *args):
        self.connection._notice_handlers.remove(self.handler)


    def handler(self, diag: Diagnostic):
        return pg_notice_handler(diag, logger=self.logger)


def pg_notice_handler(diag: Diagnostic, logger: logging.Logger = None):
    """
    Handler required by psycopg 3 `connection.add_notice_handler()`.
    """
    # determine level
    level = pg_get_logging_level(diag.severity_nonlocalized)
    
    # determine logger
    if logger:
        logger = logger
        message = diag.message_primary
    else:
        # parse context
        m = re.match(r"^fonction [^\s]+ (\w+)", diag.context or '')
        if m:
            logger = logging.getLogger(f"pg:{m[1]}")
            message = diag.message_primary
        else:
            logger = logging.getLogger("pg")
            message = f"{diag.context or ''}{diag.message_primary}"

    # write log
    logger.log(level, message)


class Pg2NoticeHandler:
    """
    This class is the actual handler required by psycopg 2 `connection.notices`.
    
    It can also be used as a context manager that remove the handler on exit.
    """
    _pg_msg_re = re.compile(r"^(?P<pglevel>[A-Z]+)\:\s(?P<message>.+(?:\r?\n.*)*)$", re.MULTILINE)

    def __init__(self, connection, logprefix: str = None):
        self.connection = connection
        self.logger = logging.getLogger(logprefix if logprefix else 'pg')
        self.connection.notices = self

    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.connection.notices = []

        
    def append(self, fullmsg: str):
        fullmsg = fullmsg.strip()
        m = self._pg_msg_re.match(fullmsg)
        if not m:
            self.logger.error(fullmsg)
            return

        message = m.group("message").strip()
        severity = m.group("pglevel")
        level = pg_get_logging_level(severity)

        self.logger.log(level, message)


def pg_get_logging_level(severity_nonlocalized: str):
    if severity_nonlocalized.startswith('DEBUG'): # not sent to client (by default)
        return logging.DEBUG
    elif severity_nonlocalized == 'LOG': # not sent to client (by default), written on server log (LOG > ERROR for log_min_messages)
        return logging.DEBUG
    elif severity_nonlocalized == 'NOTICE': # sent to client (by default) [=client_min_messages]
        return logging.DEBUG
    elif severity_nonlocalized == 'INFO': # always sent to client
        return logging.INFO
    elif severity_nonlocalized == 'WARNING': # sent to client (by default) [=log_min_messages]
        return logging.WARNING
    elif severity_nonlocalized in ['ERROR', 'FATAL']: # sent to client
        return logging.ERROR
    elif severity_nonlocalized in 'PANIC': # sent to client
        return logging.CRITICAL
    else:
        return logging.ERROR


OID_CATALOG = {
    16: ('bool', bool),
    17: ('bytea', bytes),
    18: ('char', str),
    19: ('name', str),
    20: ('int8', int),
    21: ('int2', int),
    23: ('int4', int),
    25: ('text', str),
    26: ('oid', int),
    114: ('json', None),
    650: ('cidr', None),
    700: ('float4', float),
    701: ('float8', float),
    869: ('inet', None),
    1042: ('bpchar', str),
    1043: ('varchar', str),
    1082: ('date', date),
    1083: ('time', time),
    1114: ('timestamp', datetime),
    1184: ('timestamptz', datetime),
    1186: ('interval', None),
    1266: ('timetz', time),
    1700: ('numeric', Decimal),
    2249: ('record', None),
    2950: ('uuid', UUID),
    3802: ('jsonb', None),
    3904: ('int4range', None),
    3906: ('numrange', None),
    3908: ('tsrange', None),
    3910: ('tstzrange', None),
    3912: ('daterange', None),
    3926: ('int8range', None),
    4451: ('int4multirange', None),
    4532: ('nummultirange', None),
    4533: ('tsmultirange', None),
    4534: ('tstzmultirange', None),
    4535: ('datemultirange', None),
    4536: ('int8multirange', None),
}
