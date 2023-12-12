
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



class EditProfile(Resource):

    def post(self):
        try:
            description = request.form.get('description')
            name = request.form.get('name')
            id = request.form.get('user_id')


            nameInUse = User.query.filter(User.name == name, User.id != id).first()
            if nameInUse:
                flash('Username already in use')
                return redirect(url_for('user.editprofile'))

            picture = request.files['picture']
            filename = secure_filename(picture.filename)


            user = User.query.get(id)  # Retrieve the user by id

            if user:
                user.description = description  # Update the description
                user.name = name  # Update the name


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
                    user.profilepicture = picture_filename  # Update the profile picture



                db.session.commit()  # Commit the changes to the database

                return redirect(url_for('user.profile_id', user_name=user.name))  # Redirect to the profile page'))            
            else:
                return jsonify(error='User not found'), 404
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify(error=error), 400
