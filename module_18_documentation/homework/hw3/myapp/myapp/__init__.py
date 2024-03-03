import config
import logging

from flask import Flask
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_object(config.CONFIG)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# Логирование
handler = RotatingFileHandler(app.config['LOG_FILE'],
    maxBytes=app.config['LOG_FILE_SIZE']*1024*1024,
    backupCount=1)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(app.config['LONG_LOG_FORMAT'])
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# API
from myapp import ns_api

from myapp import views