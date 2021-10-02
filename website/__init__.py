from flask import Flask
import os


def create_app():
    '''
        initiates a flask object returns it
    '''
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('flask_secret_key')

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
