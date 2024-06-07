from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

from .database import db


toolbar = DebugToolbarExtension()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///prod.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SECRET_KEY'] = 'key'
    db.init_app(app)
    toolbar.init_app(app)

    from .models import Client, Parking, ClientParking

    with app.app_context():
        db.drop_all()
        db.create_all()
        from .routes import get_clients_list

    return app
