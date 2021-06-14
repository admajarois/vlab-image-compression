from projects.image_decompression import image_decompression
import os
from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, request, url_for, flash
import os
from werkzeug.utils import secure_filename
from projects import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, image_compression, image_decompression, image_restorer

vlab = Blueprint('vlab', __name__)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@vlab.route('/eksperimen', methods=['GET', 'POST'])
@login_required
def eksperimen():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('Tidak ada file untuk diproses', category='error')
            return redirect(request.url)
        file = request.files['image']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            app = os.path.join(UPLOAD_FOLDER, filename)
            compress = image_compression.image_compression(app)
            decompress = image_decompression.image_decompression(app)
            restorer = image_restorer.channel_restorer(app)
            # print(compress)
         
            bit_stream, ratio, redudance = compress
            pixel_stream = decompress
            total_loss, original_image_dimension, restore_image_dimension = restorer
            # return redirect(url_for('vlab.eksperimen'))
            return render_template('eksperimen.html',filename=filename, title="Program kompresi", app=app, bit=bit_stream, ratio=ratio, 
            pixel=pixel_stream, user=current_user,redudance=redudance, total_loss=total_loss, original_image_dimension=original_image_dimension, restore_image_dimension=restore_image_dimension)
            
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