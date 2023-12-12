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
from flask import flash


class CreatePost(Resource):


    def post(self):
        try:
            description = request.form.get('description')
            user_id = request.form.get('user_id')

            picture = request.files['picture']
            filename = secure_filename(picture.filename)
            # os.SEEK_END == 2
            # seek() return the new absolute position
            file_length = picture.seek(0, os.SEEK_END)
            print("file length is ", file_length)
            # also can use tell() to get current position
            # file_length = file.tell()

            # seek back to start position of stream, 
            # otherwise save() will write a 0 byte file
            # os.SEEK_END == 0
            picture.seek(0, os.SEEK_SET)

            current_time = datetime.datetime.now()



            if filename != '':
                print(f"Uploaded file size: {picture.content_length}")  # Debug print
                if file_length > 25 * 1024 * 1024:  # 1MB limit for testing
                    flash('File size exceeds the limit of 25MB.')
                    return redirect(url_for('user.createpost'))

                picture_path = os.path.join('Code/website/static/uploads', filename)
                count = 1
                while os.path.exists(picture_path):
                    # Add a number to the front of the filename
                    filename = f"{count}{filename}"
                    picture_path = os.path.join('Code/website/static/uploads', filename)
                    count += 1

                picture.save(picture_path)
                picture_filename = filename            
                new_post = Post(user_id=user_id, description=description , picture=picture_filename, date = current_time)
                
                db.session.add(new_post)
                db.session.commit()
                return redirect(url_for('user.index'))
                
                
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify(error=error), 400
