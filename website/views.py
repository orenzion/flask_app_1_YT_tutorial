from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/')
@login_required  # makes sure a user cant acceess the homepage unless he is logged in
def home():
    return render_template("home.jinja", user=current_user)
