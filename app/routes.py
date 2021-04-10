from app import app
from flask import render_template, redirect, request, url_for
from werkzeug.utils import secure_filename

@app.route('/')
@app.route('/index')
def index():

    greeting = 'Hello Dunia!'

    return render_template('index.html', title='Hello', greeting=greeting)

@app.route('/compress')
def compress():

    compress = 'halaman compress'

    return render_template('compress.html',title='compressing', compress=compress)




