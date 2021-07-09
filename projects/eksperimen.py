from projects.functions.image_compressor import compressor
from projects.models import Image
from projects.image_decompression import image_decompression
import os
from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, request, url_for, flash
import os
import time
from werkzeug.utils import secure_filename
from projects import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, image_compression, image_decompression, image_restorer

vlab = Blueprint('vlab', __name__)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@vlab.route('/eksperimen/<int:id>', methods=['GET', 'POST'])
@vlab.route('/eksperimen', methods=['GET', 'POST'])
@login_required
def eksperimen(id=None):
    images = Image.query.all()
    image = Image.query.filter_by(id=id).first()
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('Tidak ada file untuk diproses', category='error')
            return redirect(request.url)
        file = request.files['image']

        if file and allowed_file(file.filename):
            start_times = time.time()
            
            filename = secure_filename(file.filename)
            user_file = UPLOAD_FOLDER+'/'+current_user.NIM
            if os.path.exists(user_file) == False:
                os.mkdir(user_file)
            file.save(os.path.join(user_file, filename))

            app = os.path.join(user_file, filename)
            compress = image_compression.image_compression(app)
            decompress = image_decompression.image_decompression(app)
            restorer = image_restorer.restorer(app)
            # print(compress)
         
            bit_stream, ratio, rmse, relative_redudance = compress
            pixel_stream = decompress
            total_loss, original_image_dimension, restore_image_dimension = restorer
            end_times = time.time()
            times = end_times-start_times
            return render_template('eksperimen.html',times=times,filename=filename, title="Program kompresi", app=app, bit=bit_stream, ratio=ratio, 
            pixel=pixel_stream, user=current_user,rmse = rmse, redudance = relative_redudance, total_loss=total_loss, original_image_dimension=original_image_dimension, restore_image_dimension=restore_image_dimension, images=images)
    else:
        if image:
            filename = secure_filename(image.image)
            app = os.path.join(UPLOAD_FOLDER, filename)
            compress = image_compression.grayscale_compression(app)
            gray_bit_stream, compresstion_ratio, reversed_coded_gray, gray_coded_pixel = compress
            decompress = image_decompression.gray_decompression(app, gray_bit_stream, reversed_coded_gray)
            gray_pixel_stream = decompress
            return render_template('eksperimen.html', title="Program Kompresi", user=current_user, bit_stream = gray_bit_stream, ratio=compresstion_ratio,
        gray_pixel=gray_pixel_stream, image = image, images=images, code_pixel = gray_coded_pixel)
    
    return render_template('eksperimen.html',title="Program Kompresi", user=current_user, images=images)