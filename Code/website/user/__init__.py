from flask import Blueprint, render_template
from flask_login import login_required, current_user
import os



user = Blueprint('user', __name__, template_folder='templates')

@user.route('/')
def index():
    return render_template('index.html')

@user.route('/profile')
@login_required
def profile():
    return render_template('profile.html' , name=current_user.name)