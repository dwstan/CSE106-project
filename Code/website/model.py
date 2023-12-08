from flask_sqlalchemy import SQLAlchemy
import os
from time import time
from flask_login import UserMixin


db = SQLAlchemy()






class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    profilepicture = db.Column(db.String(1000), default="default.png")
