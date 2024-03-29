import cv2
import numpy as np

def decoder (image, bit_stream, red_stream_decoder, green_stream_decoder, blue_stream_decoder):
    code_stream = bit_stream_decode(image)
    if code_stream == []:
        while code_search(bit_stream, red_stream_decoder, 5) != 'seperator':
            code = code_search(bit_stream, red_stream_decoder, 5)
            code_stream.append(red_stream_decoder[code])
            bit_stream = bit_stream.replace(code, '', 1)

        code = code_search(bit_stream, red_stream_decoder, 5)
        bit_stream = bit_stream.replace(code, '', 1)
        print('Red over, Green started')

        while code_search(bit_stream, green_stream_decoder, 5) != 'seperator':
            code = code_search(bit_stream, green_stream_decoder, 5)
            code_stream.append(green_stream_decoder[code])
            bit_stream = bit_stream.replace(code, '', 1)

        code = code_search(bit_stream, green_stream_decoder, 5)
        bit_stream = bit_stream.replace(code, '', 1)
        print('Green over, Blue started')

        while bit_stream != '':
            code = code_search(bit_stream, blue_stream_decoder, 5)
            code_stream.append(blue_stream_decoder[code])
            bit_stream = bit_stream.replace(code, '', 1)

    return code_stream

def gray_decoder(image, bit_stream, gray_decoder):
    gray_code_stream = gray_bit_stream_decode(image)
    if gray_code_stream == []:
        while code_search(bit_stream, gray_decoder, 5) != 'seperator':
            code = code_search(bit_stream, gray_decoder, 5)
            gray_code_stream.append(gray_decoder[code])
            bit_stream = bit_stream.replace(code, '', 1)

        code = code_search(bit_stream, gray_decoder, 5)
        bit_stream = bit_stream.replace(code, '', 1)
        print('Gray, done!')
    return gray_code_stream

def code_search (small_bit_stream, search_dict, slicing_index):
    code = small_bit_stream[:slicing_index]
    if search_dict.get(code, None) == None:
        return code_search(small_bit_stream, search_dict, slicing_index + 1)
    else:
        return code

def bit_stream_decode (image):
    file_to_be_decoded = cv2.imread(image)
    file_to_be_decoded = cv2.cvtColor(file_to_be_decoded, cv2.COLOR_BGR2RGB)
    
    file_x, file_y, file_z = file_to_be_decoded.shape
    file_size = file_x*file_y*file_z
    
    decoded_stream = []
    for z in range(file_z):
        for x in range(file_x):
            for y in range(file_y):
                decoded_stream.append(file_to_be_decoded[x][y][z])
    
    return decoded_stream

def gray_bit_stream_decode(image):
    gray_to_be_decoded = cv2.imread(image)
    gray_to_be_decoded = cv2.cvtColor(gray_to_be_decoded, cv2.COLOR_BGR2GRAY)

    file_x, file_y = gray_to_be_decoded.shape
    file_size = file_x*file_y

    gray_decode_stream = []

    for x in range(file_x):
        for y in range(file_y):
            gray_decode_stream.append(gray_to_be_decoded[x][y])
    
    return gray_decode_stream