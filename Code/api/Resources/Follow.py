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
            print(follower_id, followed_id)
            sql = text("""DELETE FROM follow WHERE follower_id = :follower_id AND followed_id = :followed_id""")
            input_params = {'follower_id': follower_id, 'followed_id': followed_id}
            db.session.execute(sql, input_params)
            db.session.commit()

            return 200
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify(error=error), 400

        

    def post(self):
        try:

            follower_id = request.form.get('user_id')
            followed_id = request.form.get('profile_id')

           
            sql = text("""SELECT COUNT(*) FROM follow WHERE follower_id = :follower_id AND followed_id = :followed_id""")
            
            input_params = {'follower_id': follower_id, 'followed_id': followed_id}
            result = db.session.execute(sql, input_params)
            result = result.scalar()

            if result == 0:
            
                sql = text("""
                    INSERT OR IGNORE INTO follow (follower_id, followed_id)
                    VALUES (:follower_id, :followed_id)
                """)

                input_params = {'follower_id': follower_id, 'followed_id': followed_id}
                db.session.execute(sql, input_params)
                db.session.commit()

            return redirect(url_for('user.index'))
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify(error=error), 400