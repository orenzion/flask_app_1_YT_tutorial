from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    # init a flask object
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('flask_secret_key')

    # configure and attach the db to the flask app
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # import the blueprint objects so that we can register them to the flask app
    from .views import views
    from .auth import auth

    # register the blueprints with the flask app
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # we import .models and the objects from it just to make sure we define them before we create the DB
    from .models import User, Note

    create_database(app)

    # initiate the login manager after creating the db
    # init a login manager
    login_manager = LoginManager()
    # tell flask where to redirect a user incase he is not logged in
    login_manager.login_view = 'auth.login'
    # attach the flask app to the login manager (there can be multiple apps)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    # check first if db exists
    if not path.exists('website/' + DB_NAME):
        # create db and register the flask app
        db.create_all(app=app)
        print('Created Database!')
