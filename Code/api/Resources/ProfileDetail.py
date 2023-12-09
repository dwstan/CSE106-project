# get followers from follwers table by counting where followed_id = user_id
# get following from follwers table by counting where follower_id = user_id
# get posts from posts table by counting where user_id = user_id
# 
# 
# 
# 
# 

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
from werkzeug.utils import secure_filename


class ProfileDetail(Resource):
    def get(self, user_name):
        try: 

            sql = text("""SELECT id, profilepicture, description FROM user WHERE name = :user_name""")
            input_params = {'user_name': user_name}
            result = db.session.execute(sql, input_params)
            result = result.fetchone()

            user_id = result[0]

            sql = text("""
                SELECT count(*)
                FROM follow
                WHERE followed_id = :user_id    
            """)

            input_params = {'user_id': user_id}
            results = db.session.execute(sql, input_params)
            followers = results.scalar()

            sql = text("""
                SELECT count(*)
                FROM follow
                WHERE follower_id = :user_id
            """)
            input_params = {'user_id': user_id}
            results = db.session.execute(sql, input_params)
            following = results.scalar()

            sql = text("""
                SELECT count(*)
                FROM post
                WHERE user_id = :user_id
            """)
            input_params = {'user_id': user_id}
            results = db.session.execute(sql, input_params)
            posts = results.scalar()



            response = {
                'user_id': result[0],
                'profilepicture': result[1],
                'description': result[2],
                'followers': followers,
                'following': following,
                'posts': posts,

                'name': user_name
            }

        
        except SQLAlchemyError as e:
            abort(500, error='Could not process request')

        return jsonify(response)


