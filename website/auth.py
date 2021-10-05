from flask import Blueprint, render_template, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.jinja", text="Testing", boolean=True)


@auth.route('/logout')
def logout():
    return "<p>logout.html</p>"


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('email must be greater than 3 characters.', category='error')
        elif len(firstName) < 2:
            flash('firstName must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('password must be at least 7 characters.', category='error')
        else:
            # create new user
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(
                password1, method='sha256'))
            # add new user to db
            db.session.add(new_user)
            # commit transaction
            db.session.commit()
            # notify user with flash message
            flash('Account Created.', category='success')

    return render_template("sign_up.jinja")
