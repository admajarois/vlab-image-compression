from flask_login import login_user, login_required, logout_user
from flask_login.utils import decode_cookie
from projects.models import Kelas, Role, Users
from projects.functions import delete_dir
from projects import db
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash


auth  = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    greeting = 'Login'
    if request.method == 'POST':
        nim = request.form.get('nim')
        password = request.form.get('password')
        user = Users.query.filter_by(NIM=nim).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Login Berhasil', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
                flash('Password salah', category='error')
                return redirect(url_for('auth.login'))
        else:
            flash('anda tidak terdaftar, silahkan daftar!', category='error')
    
    return render_template('login.html', greeting=greeting)
    
    

@auth.route('/register',  methods=['GET', 'POST'])
def register():
    greeting = 'Daftar'
    daftar_kelas = Kelas.query.all()
    if request.method == 'POST':
        email = request.form.get('email')
        nama = request.form.get('nama')
        kelas = request.form.get('kelas')
        nim = request.form.get('NIM')
        password = request.form.get('password')
        password2 = request.form.get('confirm-password')

        user = Users.query.filter_by(NIM=nim).first()
        if user:
            flash('NIM anda sudah terdaftar', category='error')
        elif nim == '' :
            flash('NIM tidak boleh kosong', category='error')
        elif len(nama) < 2:
            flash('Nama harus lebih dari 2 karakter dan tidak boleh kosong', category='error')
        elif len(email) < 4:
            flash('Email harus lebih dari 4 dan tidak boleh kosong', category='error')
        elif len(password) < 8:
            flash('Password harus lebih dari 8 karakter dan tidak boleh kosong')
        elif password != password2:
            flash('Password tidak sama', category='error')
        else:
            role = Role.query.filter_by(role='student').first()
            kelas = Kelas.query.filter_by(kelas=kelas).first()
            new_user = Users(NIM=nim, nama=nama, id_kelas=kelas.id,id_role=role.id, email=email, password=generate_password_hash(password, method='sha256'), image_profile="NULL")
            db.session.add(new_user)
            db.session.commit()
            flash('Akun berhasil ditambahkan!', category='success')
            return redirect(url_for('auth.login'))
            

    return render_template('register.html', title=greeting, daftar_kelas=daftar_kelas)

@auth.route('/logout')
@login_required
def logout():
    delete_dir.delete_dir()
    delete_dir.del_user_dir()
    logout_user()
    return redirect(url_for('views.index'))