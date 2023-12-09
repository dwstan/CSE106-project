from flask import jsonify, request, redirect, url_for, flash
from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from website.model import db, User, Post
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


class CreatePost(Resource):


    def post(self):
        try:
            description = request.form.get('description')
            user_id = request.form.get('user_id')

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
                new_post = Post(user_id=user_id, description=description , picture=picture_filename)
                
                db.session.add(new_post)
                db.session.commit()
                return redirect(url_for('user.index'))
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify(error=error), 400
