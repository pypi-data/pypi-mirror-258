from __future__ import annotations

import logging
import logging.config
import os
import sys
from atexit import register as atexit_register

from .colors import Color

try:
    from systemd.journal import JournalHandler
    _systemd_available = True
except ImportError:
    _systemd_available = False


def configure_logging(prog: str = None, *, systemd: bool = False, count: bool = True):
    """
    Logging configuration (suitable by default for console applications).
    """
    config = get_logging_dict_config(prog, systemd=systemd, count=count)

    logging.config.dictConfig(config)
    

def get_logging_dict_config(prog: str = None, *, systemd: bool = False, count: bool = True):
    """
    Logging configuration (suitable by default for Django applications).
    """
    console_level, console_levelnum = _get_level_from_env('LOG_LEVEL', 'INFO')
    log_file_level, log_file_levelnum = _get_level_from_env('LOG_FILE_LEVEL')

    log_file = os.environ.get('LOG_FILE', None)
    if log_file or log_file_level or systemd:
        # Determine default prog if not given
        if not prog:
            path = sys.argv[0]
            if path.endswith('__main__.py'):
                path = path[:-len('__main__.py')]
            if path.endswith(('/', '\\')):
                path = path[:-1]

            prog = os.path.basename(path)
            if prog.endswith('.py'):
                prog = prog[:-len('.py')]

    if log_file or log_file_level:
        if not log_file:
            log_file = f"{prog}.log"
        elif log_file.upper() in ['1', 'TRUE']:
            log_file = f"{prog}.log"
        elif log_file.upper() in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']:
            if not log_file_level:
                log_file_level = log_file.upper()
                log_file_levelnum = logging.getLevelName(log_file_level)
            log_file = f"{prog}.log"
        else:
            if not log_file_level:
                log_file_level = 'INFO'
                log_file_levelnum = logging.getLevelName(log_file_level)

    root_level = log_file_level if log_file_levelnum is not None and log_file_levelnum < console_levelnum else console_level

    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'console': {
                '()': ColoredFormatter.__module__ + '.' + ColoredFormatter.__qualname__,
                'format': '%(levelcolor)s%(levelname)s%(reset)s %(gray)s[%(name)s]%(reset)s %(messagecolor)s%(message)s%(reset)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'console',
                'level': console_level,
            },
        },
        'root': {
            'handlers': ['console'],
            'level': root_level,
        },
        'loggers': {
            'django': { 'level': os.environ.get('DJANGO_LOG_LEVEL', '').upper() or 'INFO', 'propagate': False },
            'smbprotocol': { 'level': 'WARNING' },
        },
    }

    if count:
        config['handlers']['count'] = {
            'class': CountHandler.__module__ + '.' + CountHandler.__qualname__,
            'level': 'WARNING',
        }

        config['root']['handlers'].append('count')

    if log_file:
        config['formatters']['file'] = {
            'format': '%(asctime)s %(levelname)s [%(name)s] %(message)s',
        }

        config['handlers']['file'] = {
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': log_file,
            'mode': 'a',
            'level': log_file_level or root_level,
        }

        config['root']['handlers'].append('file')

    if systemd:
        if not _systemd_available:
            raise ValueError(f"cannot use systemd: not available")
        
        config['formatters']['systemd'] = {
            'format': '%(levelname)s [%(name)s] %(message)s',
        }

        config["handlers"]["systemd"] = {
            "class": "systemd.journal.JournalHandler",
            "SYSLOG_IDENTIFIER": prog,
        }

        config["root"]["handlers"].append("systemd")

    return config


def _get_level_from_env(varname: str = None, default: str = None) -> tuple[str,int|None]:
    level = os.environ.get(varname, '').upper() or default
    if not level:
        return ('', None)

    levelnum = logging.getLevelName(level)
    
    if not isinstance(levelnum, int):
        print(f"warning: invalid {varname} \"{level}\": fall back to \"{default or 'INFO'}\"")
        level = default or 'INFO'
        levelnum = logging.getLevelName(level)

    return (level, levelnum)


class ColoredRecord:
    LEVELCOLORS = {
        logging.DEBUG:     Color.GRAY,
        logging.INFO:      Color.CYAN,
        logging.WARNING:   Color.YELLOW,
        logging.ERROR:     Color.RED,
        logging.CRITICAL:  Color.BOLD_RED,
    }

    MESSAGECOLORS = {
        logging.INFO:      '',
    }

    def __init__(self, record: logging.LogRecord):
        # The internal dict is used by Python logging library when formatting the message.
        # (inspired from library "colorlog").
        levelcolor = self.LEVELCOLORS.get(record.levelno, '')
        self.__dict__.update(record.__dict__)
        self.__dict__.update({
            'levelcolor': levelcolor,
            'messagecolor': self.MESSAGECOLORS.get(record.levelno, levelcolor),
            'red': Color.RED,
            'green': Color.GREEN,
            'yellow': Color.YELLOW,
            'cyan': Color.CYAN,
            'gray': Color.GRAY,
            'bold_red': Color.BOLD_RED,
            'reset': Color.RESET,
        })


class ColoredFormatter(logging.Formatter):
    def formatMessage(self, record: logging.LogRecord) -> str:
        """Format a message from a record object."""
        wrapper = ColoredRecord(record)
        message = super().formatMessage(wrapper)
        return message


class CountHandler(logging.Handler):
    counts: dict[int, int]
    
    _for_exit_counts: dict[int, int] = {}
    _detected_exit_code = 0
    _original_exit_func = sys.exit
    _already_registered = False

    def __init__(self, level=logging.WARNING, atexit=True):
        self.counts = {}
        self.atexit = atexit

        if self.atexit:
            if not self._already_registered:
                sys.exit = self._detecting_exit_func
                atexit_register(self._exit_callback)
                type(self)._already_registered = True
        
        super().__init__(level=level)

    def emit(self, record: logging.LogRecord):
        if record.levelno >= self.level:
            if not record.levelno in self.counts:
                self.counts[record.levelno] = 1
            else:
                self.counts[record.levelno] += 1
            
            if self.atexit:
                if not record.levelno in self._for_exit_counts:
                    self._for_exit_counts[record.levelno] = 1
                else:
                    self._for_exit_counts[record.levelno] += 1

    @classmethod
    def _detecting_exit_func(cls, code: int = 0):
        cls._detected_exit_code = code
        cls._original_exit_func(code)

    @classmethod
    def _exit_callback(cls):
        msg = ""

        levelnos = sorted(cls._for_exit_counts.keys(), reverse=True)
        for levelno in levelnos:
            levelname = logging.getLevelName(levelno)
            levelcolor = ColoredRecord.LEVELCOLORS.get(levelno, '')
            msg += (", " if msg else "") + f"{levelcolor}%s{Color.RESET}" % levelname + ": %d" % cls._for_exit_counts[levelno]

        if msg:
            print("Logged " + msg, file=sys.stderr)
            # Change exit code if it was not originally set explicitely to another value, using `sys.exit()`
            if cls._detected_exit_code == 0:
                os._exit(68) # EADV (Advertise error)
