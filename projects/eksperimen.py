from flask.helpers import flash
import os
from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename
from projects import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, image_compression
from projects import image_compression

vlab = Blueprint('vlab', __name__)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@vlab.route('/eksperimen', methods=['GET', 'POST'])
@login_required
def eksperimen():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('Tidak ada file')
            return redirect(request.url)
        file = request.files['image']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            app = os.path.join(UPLOAD_FOLDER, filename)
            compress = image_compression.image_compression(app)
            # print(compress)
            # app=image_compression.image_compression(filename)
            bit_stream, ratio = compress
            # return redirect(url_for('vlab.eksperimen'))
            return render_template('eksperimen.html', title="Program kompresi", filename = filename, bit=bit_stream, ratio=ratio, user=current_user)
            
    return render_template('eksperimen.html',title="Program Kompresi", user=current_user)



# @views.route('/eksperimen', methods=['GET', 'POST'])
# @login_required
# def eksperimen():
#     if request.method == 'POST':
#         if 'image' not in request.files:
#             flash('Tidak ada file')
#             return redirect(request.url)
#         file = request.files['image']

#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(UPLOAD_FOLDER, filename))
            
#             return redirect(url_for('views.eksperimen', name=filename))
#     return render_template('eksperimen.html',title="Program Kompresi", user=current_user)