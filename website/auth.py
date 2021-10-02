from flask import Blueprint

auth = Blueprint('auth', __name__)


@auth.route('/Login')
def login():
    return "<p>Login</p>"


@auth.route('/Logout')
def logout():
    return "<p>Logout</p>"


@auth.route('/sign-up')
def sign_up():
    return "<p>Sign Up</p>"
