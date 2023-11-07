import logging
import sys
import string


class CustomFileHandler(logging.Handler):
    def __init__(self, mode='a'):
        super().__init__()
        self.filename = None
        self.mode = mode

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        self.filename = f'{record.module}-{record.levelname.lower()}.log'
        with open(self.filename, mode=self.mode) as f:
            f.write(message + '\n')


class ASCIIFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        message: str = record.msg
        if isinstance(message, str):
            if not is_ascii(message):
                return False
        return True


def is_ascii(strng: str):
    return all(map(lambda x: x in string.printable, strng))


# def config_logger(loger, level):
#     formatter = logging.Formatter(fmt='%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s')
#
#     stream_handler = logging.StreamHandler(stream=sys.stdout)
#     stream_handler.setLevel(level)
#     stream_handler.setFormatter(formatter)
#
#     custom_file_handler = CustomFileHandler()
#     custom_file_handler.setLevel(level)
#     custom_file_handler.setFormatter(formatter)
#
#     loger.setLevel(level)
#     loger.addHandler(stream_handler)
#     loger.addHandler(custom_file_handler)


dict_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'base': {
            'format': '%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'level': 'DEBUG',
            'formatter': 'base',
            'filters': ['ascii_filter']
        },
        'custom_file': {
            '()': CustomFileHandler,
            'level': 'DEBUG',
            'formatter': 'base',
            'filters': ['ascii_filter']
        },
        'rotating_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            'formatter': 'base',
            'filename': 'utils.log',
            'when': 'h',
            'interval': 10,
            'backupCount': 5,
            'filters': ['ascii_filter']
        },
        'http': {
            'class': 'logging.handlers.HTTPHandler',
            'host': '127.0.0.1:3000',
            'url': '/log',
            'method': 'POST',
            'level': 'DEBUG',
            'filters': ['ascii_filter']
        }
    },
    'filters': {
        'ascii_filter': {
            '()': ASCIIFilter
        }
    },
    'loggers': {
        'app': {
            'level': 'DEBUG',
            'handlers': ['console', 'custom_file', 'http'],
            'propagate': False
        },
        'utils': {
            'level': 'INFO',
            'handlers': ['rotating_file', 'http'],
            'propagate': False
        }
    }
}


dict_config_from_ini = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'fileFormatter': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S%Z'
        },
        'consoleFormatter': {
            'format': '%(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S%Z'
        }
    },
    'handlers': {
        'consoleHandler': {
            'class': 'logging.StreamHandler',
            'level': 'WARNING',
            'formatter': 'consoleFormatter',
            'stream': (sys.stdout,)
        },
        'fileHandler': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'fileFormatter',
            'filename': 'logfile.log'
        }
    },
    'loggers': {
        'appLogger': {
            'level': 'DEBUG',
            'handlers': ['consoleHandler', 'fileHandler'],
            'qualname': 'appLogger',
            'propagate': True
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['consoleHandler']
    },
}
