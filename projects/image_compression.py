import os
import cv2
import numpy as np
import json
from flask_login import current_user


from numpy.lib import math

from .functions import histogram_generator, huffman_coding, image_compressor, byte_stream_generator


def image_compression(image):
    img = cv2.imread(image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    red = img[:,:,0]
    green = img[:,:,1]
    blue = img[:,:,2]
    

    blue_histogram = histogram_generator.histogram_array_generator(blue)
    green_histogram = histogram_generator.histogram_array_generator(green)
    red_histogram = histogram_generator.histogram_array_generator(red)

    blue_probability = histogram_generator.probability_distribution_generator(blue_histogram, img.shape[0]*img.shape[1])
    green_probability = histogram_generator.probability_distribution_generator(green_histogram, img.shape[0]*img.shape[1])
    red_probability = histogram_generator.probability_distribution_generator(red_histogram, img.shape[0]*img.shape[1])

    red_probability['seperator'] = 0
    red_huffman = huffman_coding.Huffman_Coding(red_probability)
    red_coded_pixels, red_reverse_coded_pixels = red_huffman.compress()

    green_probability['seperator'] = 0
    green_huffman = huffman_coding.Huffman_Coding(green_probability)
    green_coded_pixels, green_reverse_coded_pixels = green_huffman.compress()

    blue_huffman = huffman_coding.Huffman_Coding(blue_probability)
    blue_coded_pixels, blue_reverse_coded_pixels = blue_huffman.compress()

    codes = os.path.join("projects/codes", current_user.NIM)
    decodes = os.path.join("projects/decodes", current_user.NIM)
    result = os.path.join("projects/results", current_user.NIM)
    

    # encode
    if os.path.exists(codes) == False:
        os.mkdir(codes)

    with open(codes+'/red_channel_codes.json', 'w') as fp:
        json.dump(red_coded_pixels, fp)
    with open(codes+'/green_channel_codes.json', 'w') as fp:
        json.dump(green_coded_pixels, fp)
    with open(codes+'/blue_channel_codes.json', 'w') as fp:
        json.dump(blue_coded_pixels, fp)

    # decode
    if os.path.exists(decodes) == False:
        os.mkdir(decodes)

    with open(decodes+'/red_channel_decodes.json', 'w') as fp:
        json.dump(red_reverse_coded_pixels,fp)
    with open(decodes+'/green_channel_decodes.json', 'w') as fp:
        json.dump(green_reverse_coded_pixels,fp)
    with open(decodes+'/blue_channel_decodes.json', 'w') as fp:
        json.dump(blue_reverse_coded_pixels,fp)

    red_compressed = image_compressor.compressor(red, red_coded_pixels)
    green_compressed = image_compressor.compressor(green, green_coded_pixels)
    blue_compressed = image_compressor.compressor(blue, blue_coded_pixels)

    bit_stream = byte_stream_generator.byte_stream(red_compressed, green_compressed, blue_compressed, red_coded_pixels['seperator'], green_coded_pixels['seperator'])
    
    
    compression_rasio = round((100/100-(len(bit_stream)/(img.shape[0]*img.shape[1]*img.shape[2]*8))*100/100)*100, 2)
    relative_redundance = round((1 - (1/compression_rasio))*100, 2)
    rmse = math.sqrt(1/img.shape[0]*img.shape[1]*(len(bit_stream)-img.size)**2)

    if os.path.exists(result) == False:
        os.mkdir(result)
    
    with open(result+'/bit_stream.txt', 'w') as fp:
        fp.write(bit_stream)

    return bit_stream, compression_rasio, rmse, relative_redundance

def grayscale_compression(image):
    img_gray = cv2.imread(image)
    img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
    list = []
    for i in range(img_gray.shape[0]):
        for j in range(img_gray.shape[1]):
            list.append(img_gray[i,j])
    
    gray_array = histogram_generator.pixel_frequency(list)

    gray_probability = histogram_generator.pixel_probability(gray_array, img_gray.shape[0]*img_gray.shape[1])
    gray_huffman = huffman_coding.Huffman_Coding(gray_array)
    gray_codes, gray_reverse = gray_huffman.compress()
    gray_image_compressor = image_compressor.compressor(img_gray, gray_codes)
    gray_bit_stream = byte_stream_generator.gray_byte_stream(gray_image_compressor)
    compression_ratio = (100/100-(len(gray_bit_stream)/(img_gray.shape[0]*img_gray.shape[1]*8))*100/100)*100
    result = os.path.join("projects/results", current_user.NIM)
    if os.path.exists(result) == False:
        os.mkdir(result)
    
    with open(result+'/grayscale_bit_stream.txt', 'w') as fp:
        fp.write(gray_bit_stream)
    
    
    return gray_bit_stream, compression_ratio, gray_reverse, gray_codes, gray_array, gray_probability