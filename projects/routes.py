from werkzeug.security import generate_password_hash
import projects
from projects.models import Users
from flask.helpers import flash, send_from_directory
import os
from flask_login import login_required, current_user
from projects import db
import imghdr
from flask import Blueprint, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename
from projects import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, image_compression


views = Blueprint('views', __name__)

@views.route('/')
@views.route('/index')
def index():

    greeting = 'Hello Dunia!'

    return render_template('index.html', title='Home', greeting=greeting, user=current_user)

@views.route('/materi')
@login_required
def materi():

    return render_template('materi.html', materi=materi, user=current_user)

@views.route('/pendahuluan')
@login_required
def pendahuluan():
   judul = "Pendahuluan"

   return render_template('pendahuluan.html', title=judul, user=current_user )

@views.route('/profile/<NIM>', methods=['POST', 'GET'])
@login_required
def profile(NIM):
    title = "Profile"
    if request.method == 'POST':
        nama = request.form['nama']
        prodi = request.form['prodi']
        email = request.form['email']
        password = request.form['password']

        user= Users.query.filter_by(NIM=NIM).first()
        user.nama = nama
        user.prodi = prodi
        user.email = email
        user.password = generate_password_hash(password, method='sha256')
        db.session.commit()
        return redirect(request.url)
    return render_template('profile.html', user=current_user, title=title)

@views.route('/datausers')
@login_required
def users():
    title = "Data users"
    data_user = Users.query.filter_by(role="MHS").all()
    return render_template('user.html', title=title, user=current_user, data_user=data_user)

@views.route('/delete_user/<NIM>')
@login_required
def delete_user(NIM):
    user = Users.query.filter_by(NIM=NIM).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('views.users'))

# @views.route('/update_user', methods=['POST'])
# @login_required
# def update():
    
#     return redirect(url_for('views.profile'))

@views.route('/datagambar')
@login_required
def gambar():
    title = "Data Gamabar"
    return render_template('datagambar.html', title=title, user=current_user)