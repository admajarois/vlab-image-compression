import os
from sqlalchemy.sql.expression import null
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from projects.models import Content, Role, Users, Assignment
from flask.helpers import flash
from flask_login import login_required, current_user
from datetime import datetime
from projects import UPLOAD_FOLDER, db
from flask import Blueprint, render_template, redirect, request, url_for


views = Blueprint('views', __name__)

@views.route('/')
@views.route('/index')
def index():
    greeting = 'Hello Dunia!'

    return render_template('index.html', title='Home', greeting=greeting, user=current_user)

@views.route('/materi')
@login_required
def materi():
    title = "Materi"
    return render_template('materi.html', materi=materi,title=title, user=current_user)

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
        flash('Data berhasil diubah!', category='success')
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

@views.route('/datagambar')
@login_required
def gambar():
    title = "Data Gamabar"
    return render_template('datagambar.html', title=title, user=current_user)

@views.route('/penugasan', methods=['POST', 'GET'])
@login_required
def penugasan():
    title ="Assignment"
    content = Content.query.filter_by(id_kategori=5).first()
    if request.method == 'POST':
        uploaded_file = request.files['tugas']
        filename = secure_filename(uploaded_file.filename)
        if filename != ' ':
            uploaded_file.save(os.path.join(UPLOAD_FOLDER+'/assignment', filename))
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            upload_file = Assignment(id_user=current_user.id, file_name=filename, date=date, status=null)
            db.session.add(upload_file)
            db.session.commit()
            flash('Tugas berhasil diupload!', category='success')
            return redirect(url_for('views.penugasan'))
        else:
            flash('Tidak ada file untuk diupload')
            return redirect(url_for('views.penugasan'))
    return render_template('assignment.html', title=title, user=current_user, content = content)