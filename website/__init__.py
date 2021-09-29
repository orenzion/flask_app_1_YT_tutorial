from flask import Flask
import os


def create_app():
    '''
        initiates a flask object with a secret key and returs it
    '''
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('flask_secret_key')

    return app
