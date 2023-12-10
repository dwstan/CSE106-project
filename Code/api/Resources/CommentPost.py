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



class CommentPost(Resource):
    def get(self, post_id):
        try:
            sql = text("""
                SELECT comment.id, comment.comment, comment.date, user.name, user.profilepicture, user.id
                FROM comment
                JOIN user ON comment.user_id = user.id
                WHERE comment.post_id = :post_id
                ORDER BY comment.date DESC
            """)
            input_params = {'post_id': post_id}
            results = db.session.execute(sql, input_params)
            results = results.fetchall()
            comments = [] 
            for result in results:
                comment = {
                    'id': result[0],
                    'comment': result[1],
                    'date': result[2],
                    'name': result[3],
                    'profilepicture': result[4],
                    'user_id': result[5]
                }
                comments.append(comment)
            return jsonify(comments)
        
        except SQLAlchemyError as e:

            error = str(e.__dict__['orig'])
            return jsonify(error=error), 400
