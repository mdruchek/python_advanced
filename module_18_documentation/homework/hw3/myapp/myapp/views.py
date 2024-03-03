import operator

from myapp import app
from flask import render_template


@app.route('/')
def index():
    pagedata = {}
    pagedata['title'] = app.config['TITLE']
    pagedata['data'] = {
        "A": True,
        "B": False,
        "result": True
    }
    body = render_template('index.html', pagedata=pagedata)
    return body