import os
import sys

# Конфигурация
DEBUG = True
SQLDEBUG = False

SESSION_COOKIE_NAME = 'myapp'
SESSION_TYPE = 'filesystem'

TITLE = 'Проект'

DIR_BASE = '/'.join(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/').split('/')[:-1])
DIR_DATA = DIR_BASE + '/data'
# Генерировать можно утилитой pwgen
# Пример:
# pwgen -sy 64
SECRET_KEY = '''0123456789'''

# Логирование
LOG_FILE = DIR_DATA + '/myapp.log'
LONG_LOG_FORMAT = '%(asctime)s - [%(name)s.%(levelname)s] [%(threadName)s, %(module)s.%(funcName)s@%(lineno)d] %(message)s'
LOG_FILE_SIZE = 128 # Размер файла лога в МБ