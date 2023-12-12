from flask import jsonify, request, redirect, url_for, flash
from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from website.model import db, User
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import sqlalchemy
from sqlalchemy import text
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_uploads import UploadNotAllowed
from flask_restful import Resource
from werkzeug.utils import secure_filename

import os
import os



class Signup(Resource):


    def post(self):
        try:

            # code to validate and add user to database goes here
            email = request.form.get('email')
            name = request.form.get('name')
            password = request.form.get('password')

            user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
            nameInUse = User.query.filter_by(name=name).first() # if this returns a user, then the username already exists in database

            if user: # if a user is found, we want to redirect back to signup page so user can try again
                flash('Email address already exists')
                return redirect(url_for('auth.signup'))

            if nameInUse: # if a user is found, we want to redirect back to signup page so user can try again
                flash('Username already in use')
                return redirect(url_for('auth.signup')) 



            print("picture found", request.files['picture'])
            picture = request.files['picture']
            filename = secure_filename(picture.filename)

            if filename != '':
                picture_path = os.path.join('Code/website/static/uploads', filename)
                count = 1
                while os.path.exists(picture_path):
                    # Add a number to the front of the filename
                    filename = f"{count}{filename}"
                    picture_path = os.path.join('Code/website/static/uploads', filename)
                    count += 1

                picture.save(picture_path)
                picture_filename = filename            
                new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'), profilepicture=picture_filename)
            else:
                new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))

            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('auth.login'))
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify(error=error), 400



