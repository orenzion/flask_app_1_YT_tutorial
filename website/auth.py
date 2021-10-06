from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # check if the user submited the login POST request and not the GET page request
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # query the db to check if the user exists
        user = User.query.filter_by(email=email).first()
        if user:
            # check if password is correct
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                # login the user into flask (notify the flask web server that this is the logged in user)
                # remember=True means that as long as the server is up or the user didn't clear the browser history flask will remember this user
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password. Try Again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.jinja", user=current_user)


@auth.route('/logout')
@login_required  # makes sure the user cannot access this route/page unless he is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # if its a POST method (user tries to sign up), get the variables
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # query the db to check if the user exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email Already Exists', category='error')
        elif len(email) < 4:
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
            # login the user into flask (notify the flask web server that this is the logged in user)
            # remember=True means that as long as the server is up or the user didn't clear the browser history flask will remember this user
            login_user(user, remember=True)
            # notify user with flash message
            flash('Account Created.', category='success')
            # redirect user to homepage
            # we are doing 'views.home' because views is the blueprint and home is the function corresponding to the homepage route
            # we are doing this like this because if we ever change the homepage url to something else in the views.route func this will still work
            return redirect(url_for('views.home'))

    return render_template("sign_up.jinja", user=current_user)
