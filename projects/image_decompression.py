import json
from projects.functions import bit_stream_decoder


def image_decompression(image):
    red_channel_decoder = json.load(open('./projects/decodes/red_channel_decodes.json', 'r'))
    green_channel_decoder = json.load(open('./projects/decodes/green_channel_decodes.json', 'r'))
    blue_channel_decoder = json.load(open('./projects/decodes/blue_channel_decodes.json', 'r'))
    with open('./projects/bit_stream.txt', 'r') as fr:
        bit_stream = fr.read()
    
    pixel_stream = bit_stream_decoder.decoder(image, bit_stream, red_channel_decoder, green_channel_decoder, blue_channel_decoder)
    with open('./projects/image_pixel_stream.txt', 'w') as fr:
        fr.write(str(pixel_stream))
    
    return pixel_stream