import logging
import sys


class CustomStreamHandler(logging.StreamHandler):
    def __int__(self, stream=sys.stderr):
        super().__init__()
        self.stream = stream


dict_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'base': {
            'format': '%(name)s || %(levelname)s || %(message)s || %(module)s.%(funcName)s:%(lineno)d || %(very)s'
        }
    },
    'handlers': {
        'console': {
            '()': CustomStreamHandler,
            'level': 'DEBUG',
            'formatter': 'base'
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'base',
            'filename': 'logfile.log',
            'mode': 'a'
        },
    },
    'loggers': {
        'sub_1': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False
        },
        'sub_2': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False
        }
    }
}
