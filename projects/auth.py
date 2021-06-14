from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.sql.expression import null
from werkzeug.datastructures import ViewItems
from projects.models import Users
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
            flash('NIM anda tidak terdaftar', category='error')
    
    return render_template('login.html', greeting=greeting)
    
    

@auth.route('/register',  methods=['GET', 'POST'])
def register():
    greeting = 'Daftar'
    if request.method == 'POST':
        email = request.form.get('email')
        nama = request.form.get('nama')
        nim = request.form.get('NIM')
        role = request.form.get('role')
        prodi = request.form.get('prodi')
        password = request.form.get('password')
        password2 = request.form.get('confirm-password')

        user = Users.query.filter_by(NIM=nim).first()
        if user:
            flash('NIM anda sudah terdaftar', category='error')
        elif len(email) < 4:
            flash('Email harus lebih dari 4', category='error')
        elif len(nama) < 2:
            flash('Nama harus lebih dari 2 karakter', category='error')
        elif nim == '' :
            flash('NIM tidak boleh kosong', category='error')
        elif password != password2:
            flash('Password tidak sama', category='error')
        elif len(password) < 8:
            flash('Password harus lebih dari 8 karakter')
        else:
            new_user = Users(NIM=nim, nama=nama, prodi=prodi,role=role, email=email, password=generate_password_hash(password, method='sha256'), image_profile=null)
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Akun berhasil ditambahkan!', category='success')
            return redirect(url_for('views.loginPage'))
            

    return render_template('register.html', title=greeting)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))