from flask_jsonrpc import JSONRPC

from .. import app

jsonrpc = JSONRPC(app, '/api')

from . import logic