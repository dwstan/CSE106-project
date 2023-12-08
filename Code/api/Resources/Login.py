from flask import jsonify, request, redirect, url_for, flash
from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from website.model import db, User
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import sqlalchemy
from sqlalchemy import text
from flask_login import login_user
import os

class Login(Resource):
    def post(self):
        try:
            email = request.form.get('email')
            password = request.form.get('password')
            remember = True if request.form.get('remember') else False

            user = User.query.filter_by(email=email).first()

            # check if the user actually exists
            # take the user-supplied password, hash it, and compare it to the hashed password in the database
            if not user or not check_password_hash(user.password, password):
                flash('Please check your login details and try again.')
                return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

            # if the above check passes, then we know the user has the right credentials
            login_user(user, remember=remember)
            return redirect(url_for('user.profile'))
        
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify(error=error), 400