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

class Following(Resource):
    def get(self, user_id, profile_id):
        try:
            sql = text("""SELECT COUNT(*) FROM follow WHERE follower_id = :follower_id AND followed_id = :followed_id""")
            input_params = {'follower_id': user_id, 'followed_id': profile_id}
            result = db.session.execute(sql, input_params)
            result = result.scalar()
            return jsonify(count=result)  # Update the return statement
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify(error=error), 400