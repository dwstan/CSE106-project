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

class Like(Resource):
    def delete(self):
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            post_id = data.get('post_id')

            # Delete the like relationship
            sql_delete = text("""
                DELETE FROM like WHERE user_id = :user_id AND post_id = :post_id
            """)
            input_params = {'user_id': user_id, 'post_id': post_id}
            db.session.execute(sql_delete, input_params)
            db.session.commit()

            # Get the updated like count
            sql_count = text("""
                SELECT COUNT(*) FROM like WHERE post_id = :post_id
            """)
            count_params = {'post_id': post_id}
            like_count = db.session.execute(sql_count, count_params).scalar()

            # Return a JSON response as a dictionary
            response_data = {
                "likeCount": like_count
            }
            
            return jsonify(response_data)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify(error=error), 400

    # ...

    def post(self):
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            post_id = data.get('post_id')

            # Check if the like relationship already exists
            sql_check = text("""
                SELECT COUNT(*) FROM like WHERE user_id = :user_id AND post_id = :post_id
            """)

            check_params = {'user_id': user_id, 'post_id': post_id}
            result = db.session.execute(sql_check, check_params).scalar()

            if result == 0:
                # Insert the like relationship if it doesn't exist
                sql_insert = text("""
                    INSERT INTO like (user_id, post_id) VALUES (:user_id, :post_id)
                """)

                insert_params = {'user_id': user_id, 'post_id': post_id}
                db.session.execute(sql_insert, insert_params)
                db.session.commit()

            # Get the updated like count
            sql_count = text("""
                SELECT COUNT(*) FROM like WHERE post_id = :post_id
            """)
            count_params = {'post_id': post_id}
            like_count = db.session.execute(sql_count, count_params).scalar()

            # Return a JSON response as a dictionary
            response_data = {
                "likeCount": like_count
            }

            return jsonify(response_data)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify(error=error), 400