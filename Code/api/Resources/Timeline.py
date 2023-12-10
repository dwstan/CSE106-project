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

class Timeline(Resource):
    def get(self, user_id):
        try: 
            sql = text("""
            SELECT 
                post.id, 
                post.picture, 
                post.description, 
                post.date, 
                user.name, 
                user.profilepicture,
                COALESCE(like_count.likes, 0) as like_count,
                CASE WHEN user_like.post_id IS NOT NULL THEN 1 ELSE 0 END as liked
            FROM 
                post
            JOIN 
                follow ON post.user_id = follow.followed_id
            JOIN 
                user ON user.id = follow.followed_id
            LEFT JOIN 
                (SELECT post_id, COUNT(*) as likes FROM like GROUP BY post_id) as like_count ON post.id = like_count.post_id
            LEFT JOIN 
                (SELECT post_id FROM like WHERE user_id = :profile_id) as user_like ON post.id = user_like.post_id
            WHERE 
                follow.follower_id = :profile_id
            ORDER BY 
                post.date DESC
            """)
            input_params = {'profile_id': user_id}
            results = db.session.execute(sql, input_params)
            results = results.fetchall()
            posts = [] 
            for result in results:
                post = {
                    'id': result[0],
                    'picture': result[1],
                    'description': result[2],
                    'date': result[3],
                    'name': result[4],
                    'profilepicture': result[5],
                    'like_count': result[6],
                    'liked': result[7]  # Add the liked field here
                }
                posts.append(post)
            return jsonify(posts)
                


        except SQLAlchemyError as e:

            error = str(e.__dict__['orig'])
            return jsonify(error=error), 400