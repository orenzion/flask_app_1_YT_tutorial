from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    '''
        initiates a flask object returns it
    '''
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('flask_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # we import .models and the objects from it just to make sure we define them before we create the DB
    from .models import User, Note

    create_database(app)

    return app


def create_database(app):
    # check first if db exists
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
