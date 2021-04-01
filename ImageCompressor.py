import cv2
import numpy as np
import matplotlib.pyplot as plt
import json

from functions import HistorgramGenerator, HuffmanCoding, Compressor, ByteStreamGenerator

original_image = cv2.imread('mona88.jpg')
original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
image_height = original_image.shape[0]
image_width = original_image.shape[1]

red_scaled_image = original_image[:,:,0]
green_scaled_image = original_image[:,:,1]
blue_scaled_image = original_image[:,:,2]

red_channel_histogram_array = HistorgramGenerator.histogram_array_generator(red_scaled_image)
green_channel_histogram_array = HistorgramGenerator.histogram_array_generator(green_scaled_image)
blue_channel_histogram_array = HistorgramGenerator.histogram_array_generator(blue_scaled_image)

red_channel_probability_distribution = HistorgramGenerator.probability_distribution_generator(red_channel_histogram_array, image_height*image_width)
green_channel_probability_distribution = HistorgramGenerator.probability_distribution_generator(green_channel_histogram_array, image_height*image_width)
blue_channel_probability_distribution = HistorgramGenerator.probability_distribution_generator(blue_channel_histogram_array, image_height*image_width)

red_channel_probability_distribution['seperator'] = 0
red_huffman_coding = HuffmanCoding.HuffmanCoding(red_channel_probability_distribution)
red_coded_pixels, red_reverse_coded_pixels = red_huffman_coding.compress()

green_channel_probability_distribution['seperator'] = 0
green_huffman_coding = HuffmanCoding.HuffmanCoding(green_channel_probability_distribution)
green_coded_pixels, green_reverse_coded_pixels = green_huffman_coding.compress()

blue_huffman_coding = HuffmanCoding.HuffmanCoding(blue_channel_probability_distribution)
blue_coded_pixels, blue_reverse_coded_pixels = blue_huffman_coding.compress()

with open('codes/red_channel_codes.json', 'w') as fp:
    json.dump(red_coded_pixels,fp)
with open('decodes/red_channel_decodes.json', 'w') as fp:
    json.dump(red_reverse_coded_pixels,fp)

with open('codes/green_channel_codes.json', 'w') as fp:
    json.dump(green_coded_pixels,fp)
with open('decodes/green_channel_decodes.json', 'w') as fp:
    json.dump(green_reverse_coded_pixels,fp)

with open('codes/blue_channel_codes.json', 'w') as fp:
    json.dump(blue_coded_pixels,fp)
with open('decodes/blue_channel_decodes.json', 'w') as fp:
    json.dump(blue_reverse_coded_pixels,fp)

red_channel_compressed_image = Compressor.compressor(red_scaled_image, red_coded_pixels)
green_channel_compressed_image = Compressor.compressor(green_scaled_image, green_coded_pixels)
blue_channel_compressed_image = Compressor.compressor(blue_scaled_image, blue_coded_pixels)

bit_stream = ByteStreamGenerator.byte_stream(red_channel_compressed_image, green_channel_compressed_image, blue_channel_compressed_image, red_coded_pixels['seperator'], green_coded_pixels['seperator'])

print('Compression Ratio :',(len(bit_stream) / (red_scaled_image.shape[0]*red_scaled_image.shape[1]*3*8)))
with open('ImageCompressed.txt', 'w') as fp:
    fp.write(bit_stream)