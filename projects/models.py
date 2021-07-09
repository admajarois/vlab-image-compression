from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    NIM = db.Column(db.String(11), unique=True)
    nama = db.Column(db.String(50))
    id_role = db.Column(db.Integer, db.ForeignKey('role.id'))
    id_kelas = db.Column(db.Integer, db.ForeignKey('kelas.id'))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(256))
    image_profile = db.Column(db.String(50))
    role = db.relationship('Role')
    kelas = db.relationship('Kelas')

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(10))

class Kelas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kelas = db.Column(db.String(10))

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    file_name = db.Column(db.String(50))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    status = db.Column(db.Integer)
    users = db.relationship('Users')

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_admin = db.Column(db.Integer, db.ForeignKey('admin.id'))
    image = db.Column(db.String)