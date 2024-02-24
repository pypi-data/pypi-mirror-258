from __future__ import annotations

import logging
from datetime import datetime, time, tzinfo
from pathlib import Path
from time import time_ns
from typing import Any, Callable

from ..date import is_aware, make_aware
from ..types import convert
from .utils import Row, normalize_inout, get_inout_name

logger = logging.getLogger(__name__)


class InTable:
    """
    Base class for source tables.

    The lifecycle of reading source tables is:
    1) `prepare`: perform query (on the DB server for example).
    2) `iterate`: over query results. Formatting is perform during iteration before returning the rows.
    """

    @classmethod
    def is_available(cls):
        return True
    
    def __init__(self, src, *, dir: str|Path|None = None, title: str|None = None, debug: bool = None, tz: tzinfo = None, conversions: dict[int|str,type|Callable|None] = None, **kwargs):
        if not self.is_available():
            raise ValueError(f"cannot use {type(self).__name__} (not available)")

        self.src = normalize_inout(src, dir=dir, title=title, **kwargs)
        self.name = get_inout_name(self.src)

        self._title = title
        self._debug = debug

        self._tz = tz
        """ If given (as a tzinfo or str object or 'localtime'), naive datetimes will be considered as datetimes in the given timezone. """

        self._conversions = conversions

        # set in _prepare():
        self.headers: list[str] = None
        self.prepare_duration: int = None

        # set in __iter__():
        self._extract_t0: int = None
        self.extract_duration: int = None
        self.row_count: int = None           


    def __enter__(self):
        self._print_title()

        if self._debug:
            logger.debug(f"prepare {self.name}")
            t0 = time_ns()

        self._prepare()

        # headers are now set, update conversions so that all keys are now indices instead of strings
        if self._conversions:
            new_entries = {}
            for key, formatter in self._conversions.items():
                if not isinstance(key, str):
                    continue
                try:
                    index = self.headers.index(key)
                except ValueError:
                    continue
                new_entries[index] = formatter
            
            for index, formatter in new_entries.items():
                self._conversions[index] = formatter

        if self._debug:
            self.prepare_duration = time_ns() - t0

        return self


    def __exit__(self, exc_type = None, exc_val = None, exc_tb = None):
        self._end()
        self._print_extracted_count()


    def __iter__(self):
        return self


    def __next__(self):
        if self.row_count is None:
            if self._debug:
                self._extract_t0 = time_ns()
                self.extract_duration = 0
            self.row_count = 0

        row = self._get_next_row()

        if self._debug:
            self.extract_duration = time_ns() - self._extract_t0

        self.row_count += 1

        self._format(row)

        return row


    def _print_title(self):
        if self._title is not False:
            logger.info(f"extract{f' {self._title}' if self._title else ''} from {self.name}")


    def _print_extracted_count(self):
        # symetrically to _print_title()
        if self.row_count is not None and self._title is not False:
            logger.info(f"{self.row_count:,} row{'s' if self.row_count > 1 else ''} extracted from {self.name}")

        if self._debug:
            if self.extract_duration is not None:
                logger.debug(f"total duration: {(self.prepare_duration + self.extract_duration)/1e6:,.0f} ms, prepare: {self.prepare_duration/1e6:,.0f} ms, extract: {self.extract_duration/1e6:,.0f} ms")
            else:
                logger.debug(f"duration: {self.prepare_duration/1e6:,.0f} ms")


    # -------------------------------------------------------------------------
    # For subclasses
    #

    def _prepare(self):
        pass


    def _get_next_row(self) -> Row:
        """
        Get next row. Values must be modifiable without impacting the source system. For example, ExcelTable's get_row() function must be called with the `readonly` flag.
        """
        raise StopIteration()


    def _format(self, row: Row):
        """
        Modify row values.
        """
        if self._tz or self._conversions:            
            for i, value in enumerate(row):
                if self._conversions and i in self._conversions:
                    value = convert(value, self._conversions[i])

                if self._tz and isinstance(value, (datetime,time)) and not is_aware(value):
                    value = make_aware(value, self._tz)

                row[i] = value


    def _end(self):
        pass
