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

class Follow(Resource):
    def delete(self):
        try:
            follower_id = request.form.get('user_id')
            followed_id = request.form.get('profile_id')

            # Delete the follow relationship
            sql_delete = text("""
                DELETE FROM follow WHERE follower_id = :follower_id AND followed_id = :followed_id
            """)
            input_params = {'follower_id': follower_id, 'followed_id': followed_id}
            db.session.execute(sql_delete, input_params)
            db.session.commit()

            # Get the updated follower count
            sql_count = text("""
                SELECT COUNT(*) FROM follow WHERE followed_id = :followed_id
            """)
            count_params = {'followed_id': followed_id}
            follower_count = db.session.execute(sql_count, count_params).scalar()

            # Return a JSON response as a dictionary
            response_data = {
                "followerCount": follower_count
            }
            
            return jsonify(response_data)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify(error=error), 400

    # ...

    def post(self):
        try:
            follower_id = request.form.get('user_id')
            followed_id = request.form.get('profile_id')

            # Check if the follow relationship already exists
            sql_check = text("""
                SELECT COUNT(*) FROM follow WHERE follower_id = :follower_id AND followed_id = :followed_id
            """)

            check_params = {'follower_id': follower_id, 'followed_id': followed_id}
            result = db.session.execute(sql_check, check_params).scalar()

            if result == 0:
                # Insert the follow relationship if it doesn't exist
                sql_insert = text("""
                    INSERT INTO follow (follower_id, followed_id) VALUES (:follower_id, :followed_id)
                """)

                insert_params = {'follower_id': follower_id, 'followed_id': followed_id}
                db.session.execute(sql_insert, insert_params)
                db.session.commit()

            # Get the updated follower count
            sql_count = text("""
                SELECT COUNT(*) FROM follow WHERE followed_id = :followed_id
            """)
            count_params = {'followed_id': followed_id}
            follower_count = db.session.execute(sql_count, count_params).scalar()

            # Return a JSON response as a dictionary
            response_data = {
                "followerCount": follower_count
            }

            return jsonify(response_data)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify(error=error), 400