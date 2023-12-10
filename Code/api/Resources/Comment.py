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

class Comment(Resource):
    # def delete(self):
    #     try:
    #         data = request.get_json()
    #         user_id = data.get('user_id')
    #         post_id = data.get('post_id')

    #         # Delete the like relationship
    #         sql_delete = text("""
    #             DELETE FROM like WHERE user_id = :user_id AND post_id = :post_id
    #         """)
    #         input_params = {'user_id': user_id, 'post_id': post_id}
    #         db.session.execute(sql_delete, input_params)
    #         db.session.commit()

    #         # Get the updated like count
    #         sql_count = text("""
    #             SELECT COUNT(*) FROM like WHERE post_id = :post_id
    #         """)
    #         count_params = {'post_id': post_id}
    #         like_count = db.session.execute(sql_count, count_params).scalar()

    #         # Return a JSON response as a dictionary
    #         response_data = {
    #             "likeCount": like_count
    #         }
            
    #         return jsonify(response_data)
    #     except SQLAlchemyError as e:
    #         error = str(e.__dict__['orig'])
    #         return jsonify(error=error), 400

    # ...

    def post(self):
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            post_id = data.get('post_id')
            comment = data.get('comment')
            current_time = datetime.datetime.now()

            # Insert the like relationship if it doesn't exist
            sql_insert = text("""
                INSERT INTO comment (user_id, post_id, comment, date) VALUES (:user_id, :post_id, :comment, :date)
            """)
            
            insert_params = {'user_id': user_id, 'post_id': post_id , 'comment': comment, 'date': current_time}
            db.session.execute(sql_insert, insert_params)
            db.session.commit()

            # Return a JSON response as a dictionary
            
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify(error=error)