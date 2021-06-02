import cv2
import numpy as np
import json

from projects import functions

def image_compression(image):
    original_image = cv2.imread(image)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    image_height = original_image.shape[0]
    image_width = original_image.shape[1]

    red_scale_image = original_image[:,:,0]
    green_scale_image = original_image[:,:,1]
    blue_scale_image = original_image[:,:,2]

    red_channel_histogram_array = functions.histogram_generator.histogram_array_generator(red_scale_image)
    green_channel_histogram_array = functions.histogram_generator.histogram_array_generator(green_scale_image)
    blue_channel_histogram_array = functions.histogram_generator.histogram_array_generator(blue_scale_image)

    red_channel_probability_distribution = functions.histogram_generator.probability_distribution_generator(red_channel_histogram_array, image_height*image_width)
    green_channel_probability_distribution = functions.histogram_generator.probability_distribution_generator(green_channel_histogram_array, image_height*image_width)
    blue_channel_probability_distribution = functions.histogram_generator.probability_distribution_generator(blue_channel_histogram_array, image_height*image_width)

    red_channel_probability_distribution['seperator'] = 0
    red_huffman_coding = functions.huffman_coding.Huffman_Coding(red_channel_probability_distribution)
    red_coded_pixels, red_reverse_coded_pixels = red_huffman_coding.compress()

    green_channel_probability_distribution['seperator'] = 0
    green_huffman_coding = functions.huffman_coding.Huffman_Coding(green_channel_probability_distribution)
    green_coded_pixels, green_reverse_coded_pixels = green_huffman_coding.compress()

    blue_huffman_coding = functions.huffman_coding.Huffman_Coding(blue_channel_probability_distribution)
    blue_coded_pixels, blue_reverse_coded_pixels = blue_huffman_coding.compress()

    with open('static/codes/red_channel_codes.json', 'w') as fp:
        json.dump(red_coded_pixels,fp)
    with open('static/decodes/red_channel_decodes.json', 'w') as fp:
        json.dump(red_reverse_coded_pixels,fp)

    with open('static/codes/green_channel_codes.json', 'w') as fp:
        json.dump(green_coded_pixels,fp)
    with open('static/decodes/green_channel_decodes.json', 'w') as fp:
        json.dump(green_reverse_coded_pixels,fp)

    with open('static/codes/blue_channel_codes.json', 'w') as fp:
        json.dump(blue_coded_pixels,fp)
    with open('static/decodes/blue_channel_decodes.json', 'w') as fp:
        json.dump(blue_reverse_coded_pixels,fp)

    red_channel_compressed_image = functions.image_compressor.compressor(red_scale_image, red_coded_pixels)
    green_channel_compressed_image = functions.image_compressor.compressor(green_scale_image, green_coded_pixels)
    blue_channel_compressed_image = functions.image_compressor.compressor(blue_scale_image, blue_coded_pixels)

    bit_stream = function.byte_stream_generator.byte_stream(red_channel_compressed_image, green_channel_compressed_image, blue_channel_compressed_image, red_coded_pixels['seperator'], green_coded_pixels['seperator'])

    print('Compression ratio:', (len(bit_stream)/(red_scale_image.shape[0]*red_scale_image.shape[1]*3*8)))

    with open('static/bit_stream.txt', 'w') as fp:
        fp.write(bit_stream)
