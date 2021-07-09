import json
import os
from flask_login import current_user
from projects.functions import bit_stream_decoder


def image_decompression(image):
    decodes = os.path.join("projects/decodes", current_user.NIM)
    result = os.path.join("projects/results", current_user.NIM)
    red_channel_decoder = json.load(open(decodes+'/red_channel_decodes.json', 'r'))
    green_channel_decoder = json.load(open(decodes+'/green_channel_decodes.json', 'r'))
    blue_channel_decoder = json.load(open(decodes+'/blue_channel_decodes.json', 'r'))
    with open(result+'/bit_stream.txt', 'r') as fr:
        bit_stream = fr.read()
    
    pixel_stream = bit_stream_decoder.decoder(image, bit_stream, red_channel_decoder, green_channel_decoder, blue_channel_decoder)

    # if os.path.exists(result) == False:
    #     os.mkdir(result)
    
    with open(result+'/image_pixel_stream.txt', 'w') as fr:
        fr.write(str(pixel_stream))
    
    return pixel_stream

def gray_decompression(image, gray_bit_stream, gray_decoder):
    result = os.path.join("projects/results", current_user.NIM)
    gray_pixel_stream = bit_stream_decoder.gray_decoder(image, gray_bit_stream, gray_decoder)
    with open(result+'/gray_image_pixel_stream.txt', 'w') as fr:
        fr.write(str(gray_pixel_stream))

    return gray_pixel_stream
