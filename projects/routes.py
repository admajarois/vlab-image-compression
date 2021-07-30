import os
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.functions import user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from projects.models import Content, ImageComparing, Kelas, Role, Users, Assignment
from flask.helpers import flash
from flask_login import login_required, current_user
from datetime import datetime
from projects.functions import image_comparison
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
    content = Content.query.filter_by(id=6).first()
    return render_template('materi.html', materi=materi,title=title, user=current_user, content=content)

@views.route('/pendahuluan')
@login_required
def pendahuluan():
   judul = "Pendahuluan"
   content = Content.query.filter_by(id_kategori=2).first()

   return render_template('pendahuluan.html', title=judul, user=current_user, content=content )


@views.route('/huffman_coding')
@login_required
def huffman_coding():
    judul = "Huffman Coding"
    content = Content.query.filter_by(id=7).first()

    return render_template('huffman_coding.html', user=current_user, title=judul, content=content)

@views.route('/profile/<NIM>', methods=['POST', 'GET'])
@login_required
def profile(NIM):
    title = "Profile"
    kelas = Kelas.query.all()
   
    if request.method == 'POST':
        nama = request.form['nama']
        kelas = request.form['kelas']
        email = request.form['email']
        password = request.form['password']
      
        user= Users.query.filter_by(NIM=NIM).first()
        user.nama = nama
        user.id_kelas = kelas
        user.email = email
        user.password = generate_password_hash(password, method='sha256')
        db.session.commit()
        flash('Data berhasil diubah!', category='success')
        return redirect(request.url)
    return render_template('profile.html', user=current_user, title=title, kelas=kelas)


@views.route('/penugasan', methods=['POST', 'GET'])
@login_required
def penugasan():
    title ="Assignment"
    content = Content.query.filter_by(id_kategori=5).first()
    tugas = Assignment.query.filter_by(id_user=current_user.id)
    if request.method == 'POST':
        uploaded_file = request.files['tugas']
        filename = secure_filename(uploaded_file.filename)
        if filename != ' ':
            uploaded_file.save(os.path.join(UPLOAD_FOLDER+'/assignment', filename))
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            upload_file = Assignment(id_user=current_user.id, file_name=filename, date=date, status='B')
            db.session.add(upload_file)
            db.session.commit()
            flash('Tugas berhasil diupload!', category='success')
            return redirect(url_for('views.penugasan'))
        else:
            flash('Tidak ada file untuk diupload')
            return redirect(url_for('views.penugasan'))
    return render_template('assignment.html', title=title, user=current_user, content = content, tugas=tugas)


@views.route('/perbandingan_gambar', methods=['GET', 'POST'])
@login_required
def comparison_page():
    title = "Perbandingan Gambar"
    imageori_name = None
    imagecom_name = None
    rms = None
    ssim = None

    if request.method == 'POST':
        image_ori = request.files['original_image']
        image_com = request.files['compressed_image']
        imageori_name = secure_filename(image_ori.filename)
        imagecom_name = secure_filename(image_com.filename)
 
        user_file = UPLOAD_FOLDER+'/'+current_user.NIM
        if os.path.exists(user_file) == False:
            os.mkdir(user_file)
        image_ori.save(os.path.join(user_file, imageori_name))
        image_com.save(os.path.join(user_file, imagecom_name))
        original = os.path.join(user_file, imageori_name)
        compressed = os.path.join(user_file, imagecom_name)
        compare = image_comparison.compare_images(original, compressed)

        rms, ssim = compare

        tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        save_comparison = ImageComparing(id_user=current_user.id, original_image=imageori_name, 
        compressed_image=imagecom_name, rmse=rms, ssim=ssim, tanggal=tanggal)
        db.session.add(save_comparison)
        db.session.commit()

        return render_template('comparison.html', title=title, user = current_user, rmse=rms, ssim=ssim, original=imageori_name, compressed=imagecom_name)


    return render_template('comparison.html', title=title, user=current_user,rmse=rms, ssim=ssim, original=imageori_name, compressed=imagecom_name)