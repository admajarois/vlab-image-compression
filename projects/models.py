from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    NIM = db.Column(db.String(11), unique=True)
    nama = db.Column(db.String(50))
    role = db.Column(db.String(3))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(256))
    image_profile = db.Column(db.String(50))

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    file_name = db.Column(db.String(50))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    status = db.Column(db.Integer)
    users = db.relationship('Users')