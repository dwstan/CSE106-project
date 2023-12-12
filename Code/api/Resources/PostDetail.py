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

class PostDetail(Resource):
    def get(self, post_id, user_id):
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
            LEFT JOIN 
                (SELECT post_id, COUNT(*) as likes FROM like GROUP BY post_id) as like_count ON post.id = like_count.post_id
            LEFT JOIN 
                (SELECT post_id FROM like WHERE user_id = :profile_id) as user_like ON post.id = user_like.post_id
            JOIN
                user ON post.user_id = user.id
            Where
                post.id = :post_id
            ORDER BY 
                post.date DESC
            """)
            input_params = {'post_id': post_id, 'profile_id': user_id}

            results = db.session.execute(sql, input_params)
            results = results.fetchall()
            posts = []
            for row in results:
                post = {
                    'id': row[0],
                    'picture': row[1],
                    'description': row[2],
                    'date': row[3],
                    'name': row[4],
                    'profilepicture': row[5],
                    'like_count': row[6],
                    'liked': row[7]  # Add the liked field here
                }
                posts.append(post)
            return jsonify(posts)
           
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify(error=error)