from flask import jsonify, request
from flask_restful import Resource, abort
from werkzeug.exceptions import BadRequest
from website.model import db
from sqlalchemy.exc import SQLAlchemyError
import datetime
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

import os

class UserDetail(Resource):
    def get(self, user_id):
        try:
            sql = text("""
                SELECT id, email, name, profilepicture
                FROM user
                WHERE id = :user_id       
            """)

            input_params = {'user_id': user_id}
            result = db.session.execute(sql, input_params)
            result = result.fetchone()

            if result is None:
                abort(404, error='Accessory not found')

            response = {
                'id': result[0],
                'email': result[1],
                'name': result[2],
                'profilepicture': result[3],
            }

        except SQLAlchemyError as e:
            abort(500, error='Could not process request')

        return jsonify(response)