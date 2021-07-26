from projects.functions.image_compressor import compressor
from projects.models import HistoryCompressi, Image
from projects.image_decompression import image_decompression
import os
from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, request, url_for, flash
import os
import time
from projects import db
from datetime import datetime
from werkzeug.utils import secure_filename
from projects import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, image_compression, image_decompression, image_restorer

vlab = Blueprint('vlab', __name__)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@vlab.route('/eksperimen', methods=['GET', 'POST'])
@login_required
def eksperimen():
    images = Image.query.filter_by(id=4).first()
    filename = secure_filename(images.image)
    app = os.path.join(UPLOAD_FOLDER, filename)
    compress = image_compression.grayscale_compression(app)
    gray_bit_stream, gray_compresstion_ratio, reversed_coded_gray, gray_coded_pixel, gray_array, gray_probability = compress
    decompress = image_decompression.gray_decompression(app, gray_bit_stream, reversed_coded_gray)
    gray_restorer = image_restorer.gray_restorer(app)
    gray_channel_loss, image_dimension, result_image_dimension = gray_restorer
    gray_pixel_stream = decompress
    gray_redundance = (1-1/gray_compresstion_ratio)*100
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
           
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         
            bit_stream, ratio, rmse, relative_redudance = compress
            pixel_stream = decompress
            total_loss, original_image_dimension, restore_image_dimension = restorer
            end_times = time.time()
            times = end_times-start_times
            add_history = HistoryCompressi(id_user=current_user.id, nama_gambar=filename, tinggi = original_image_dimension[0], lebar = original_image_dimension[1], channel = original_image_dimension[2], rasio_kompresi=ratio, relative_redudancy=relative_redudance, tanggal=date)
            db.session.add(add_history)
            db.session.commit()
            return render_template('eksperimen.html',times=round(times, 2),filename=filename, title="Program kompresi", app=app, bit=bit_stream, ratio=ratio, 
            pixel=pixel_stream, user=current_user,rmse = rmse, redudance = relative_redudance, total_loss=total_loss, original_image_dimension=original_image_dimension, restore_image_dimension=restore_image_dimension, 
            images=images, code_pixel = gray_coded_pixel, gray_bit_stream = gray_bit_stream, gray_pixel = gray_pixel_stream, gray_array=gray_array, gray_probability=gray_probability, sum_of_freq=sum(gray_probability.values()),
            sum_of_prob = round(sum(gray_probability.values())), gray_ratio=round(gray_compresstion_ratio, 2), gray_redundance=round(gray_redundance,2),
            gray_channel_loss = gray_channel_loss, image_dimension=image_dimension, result_image_dimension = result_image_dimension)
    
    return render_template('eksperimen.html',title="Program Kompresi", user=current_user, images=images, gray_bit_stream = gray_bit_stream, gray_ratio=round(gray_compresstion_ratio, 2),
        gray_pixel=gray_pixel_stream, code_pixel = gray_coded_pixel, gray_array=gray_array, gray_probability=gray_probability, sum_of_freq=sum(gray_array.values()),
            sum_of_prob = round(sum(gray_probability.values())), gray_redundance=round(gray_redundance,2), gray_channel_loss = gray_channel_loss, image_dimension=image_dimension, result_image_dimension = result_image_dimension)