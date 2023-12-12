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
from flask_login import current_user

from werkzeug.utils import secure_filename

import os
import os


class Search(Resource):
    def get(self,current_user_id,keyword=None):
        try:
            # Retrieve the ID of the currently logged-in user
        

            if keyword is not None:
                # If keyword is provided, filter users by the keyword and exclude the current user
                profiles = db.session.query(User).filter(User.id != current_user_id, User.name.contains(keyword)).all()
            else:
                # If keyword is not provided or is None, return all users except the current user
                profiles = db.session.query(User).filter(User.id != current_user_id).all()

            # Serialize the user profiles
            profile_list = [profile.serialize() for profile in profiles]

            return jsonify(profile_list)

        except SQLAlchemyError as e:
            # Handle SQLAlchemy errors
            return jsonify({'error': str(e)})