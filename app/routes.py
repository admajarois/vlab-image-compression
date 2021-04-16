from app import app
from flask import render_template, redirect, request, url_for
from werkzeug.utils import secure_filename

@app.route('/')
@app.route('/index')
def index():

    greeting = 'Hello Dunia!'

    return render_template('index.html', title='Hello', greeting=greeting)

@app.route('/materi')
def materi():

    return render_template('materi.html', materi=materi)

@app.route('/eksperimen')
def eksperimen():

    return render_template('eksperimen.html', eksperimen=eksperimen)

@app.route('/compress')
def compress():

    compress = 'halaman compress'

    return render_template('compress.html',title='compressing', compress=compress)

@app.route('/compress', methods=['POST'])
def upload_image():
    uploaded_image = request.files['file']
    if uploaded_image.filename != '':
        uploaded_image.save(uploaded_image.filename)
    return redirect(url_for('compress'))


