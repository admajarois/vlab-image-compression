from flask.helpers import send_from_directory
import os
from flask_login import login_required, current_user
import imghdr
from flask import Blueprint, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename
from projects import image_compression


views = Blueprint('views', __name__)

@views.route('/')
@views.route('/index')
def index():

    greeting = 'Hello Dunia!'

    return render_template('index.html', title='Home', greeting=greeting, user=current_user)

@views.route('/materi')
@login_required
def materi():

    return render_template('materi.html', materi=materi)

@views.route('/pendahuluan')
@login_required
def pendahuluan():
   judul = "Pendahuluan"

   return render_template('pendahuluan.html', title=judul, judul=judul)

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.'+(format if format != 'jpeg' else 'jpg')

@views.route('/eksperimen')
@login_required
def eksperimen():
    # image = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('eksperimen.html',title="Program Kompresi")

# @views.errorhandler(413)
# def too_large(e):
#     return "File is too large", 413


# @views.route('/upload_image', methods=['POST', 'GET'])
# def upload_image():
#    uploaded_image = request.files['file']
#    filename = secure_filename(uploaded_image.filename)
#    if filename != '':
#        file_ext = os.path.splitext(filename)[1]
#        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
#            file_ext != validate_image(uploaded_image.stream):
#            return "Invalid image", 400
        
#        uploaded_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#    return '', 204

# @views.route('/uploads/<filename>')
# def upload(filename):
#    return send_from_directory(app.config['UPLOAD_FOLDER'], filename=filename)

# @views.route('/login')
# def loginPage():
#     title = "Login"
#     return render_template('login.html', title=title)

# @views.route('/register')
# def registerPage():
#     title = "Daftar"
#     return render_template('register.html', title=title)