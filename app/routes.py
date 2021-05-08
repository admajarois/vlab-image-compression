from app import app
from flask import render_template, redirect, request, url_for
from werkzeug.utils import secure_filename
from app import image_compression

@app.route('/')
@app.route('/index')
def index():

    greeting = 'Hello Dunia!'

    return render_template('index.html', title='Home', greeting=greeting)

@app.route('/materi')
def materi():

    return render_template('materi.html', materi=materi)

@app.route('/pendahuluan')
def pendahuluan():
   judul = "Pendahuluan"

   return render_template('pendahuluan.html', title=judul, judul=judul)

@app.route('/eksperimen')
def eksperimen():

    return render_template('eksperimen.html',title="Program Kompresi", eksperimen=eksperimen)

@app.route('/compress')
def compress():

    compress = 'halaman compress'

    return render_template('compress.html',title='compressing', compress=compress)

@app.route('/proses')
def proses():

    image = url_for('static', filename='img/stones.jpg')

    image_compression.image_compression(image)

    return url_for('compress')


@app.route('/login')
def login():
    greeting = "Selamat datang!"

    return render_template('login.html', title='Login', greeting=greeting)

@app.route('/register')
def register():
    greeting = "Daftar!"

    return render_template('register.html', title='Login', greeting=greeting)
