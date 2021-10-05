from flask import Blueprint, render_template, request, flash, redirect, url_for
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
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('firstName must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('password must be at least 7 characters.', category='error')
        else:
            # create new user and hash password using a hashing algorithm
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            # add new user to db
            db.session.add(new_user)
            # commit transaction
            db.session.commit()
            # notify user with flash message
            flash('Account Created.', category='success')
            # redirect user to homepage
            # we are doing 'views.home' because views is the blue print and home is the function corresponding to the homepage route
            # we are doing this like this because if we ever change the homepage url to something else in the views.route func this will still work
            return redirect(url_for('views.home'))

    return render_template("sign_up.jinja")
