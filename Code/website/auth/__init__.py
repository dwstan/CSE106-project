from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user, logout_user
from website.model import db

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.index'))