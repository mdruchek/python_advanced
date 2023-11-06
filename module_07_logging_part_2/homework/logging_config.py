import logging
import sys
from logging.handlers import TimedRotatingFileHandler


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
            'formatter': 'base'
        },
        'custom_file': {
            '()': CustomFileHandler,
            'level': 'DEBUG',
            'formatter': 'base'
        },
        'rotating_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            'formatter': 'base',
            'filename': 'utils.log',
            'when': 'h',
            'interval': 10,
            'backupCount': 5
        }
    },
    'loggers': {
        'app': {
            'level': 'DEBUG',
            'handlers': ['console', 'custom_file'],
            'propagate': False
        },
        'utils': {
            'level': 'INFO',
            'handlers': ['rotating_file'],
            'propagate': False
        }
    }
}
