import cv2
import numpy as np
import json

from .functions import histogram_generator, huffman_coding, image_compressor, byte_stream_generator

def open_image(image):
    img = cv2.imread(image)

    blue = img[:,:,0]
    green = img[:,:,1]
    red = img[:,:,2]

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
    blue_coeded_pixels, blue_reverse_coded_pixels = blue_huffman.compress()

    # with open('./decodes/red_channel_decodes.json', 'w') as fp:
    #     json.dump(red_reverse_coded_pixels,fp)
    # with open('./decodes/green_channel_decodes.json', 'w') as fp:
    #     json.dump(green_reverse_coded_pixels,fp)
    # with open('./decodes/blue_channel_decodes.json', 'w') as fp:
    #     json.dump(blue_reverse_coded_pixels,fp)

    red_compressed = image_compressor.compressor(red, red_coded_pixels)
    green_compressed = image_compressor.compressor(green, green_coded_pixels)
    blue_compressed = image_compressor.compressor(blue, blue_coeded_pixels)

    bit_stream = byte_stream_generator.byte_stream(red_compressed, green_compressed, blue_compressed, red_coded_pixels['seperator'], green_coded_pixels['seperator'])
    
    
    compression_rasio = (len(bit_stream)/img.size)

    return bit_stream, compression_rasio

# def image_compression(self, image):
#     img = cv2.imread(image)
#     blue_histogram_array = 

# image = './uploads/stones.jpg'

# print(image_compression(image))