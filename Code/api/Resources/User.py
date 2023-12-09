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

class User(Resource):
    def get(self):
        try:
            sql = text("""
                SELECT id, email, name, profilepicture
                FROM user
            """)

            result = db.session.execute(sql)
            result = result.fetchall()

            if result is None:
                abort(404, error='Accessory not found')

            response = []
            for row in result:
                response.append({
                    'id': row[0],
                    'email': row[1],
                    'name': row[2],
                    'profilepicture': row[3],
                })

        except SQLAlchemyError as e:
            abort(500, error='Could not process request')

        return jsonify(response)