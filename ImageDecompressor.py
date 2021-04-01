import numpy as np
import matplotlib.pyplot as plt
import json


from functions import HistorgramGenerator, BitStreamDecoder

redChannelDecoder = json.load(open('./decodes/red_channel_decodes.json', 'r'))
greenChannelDecoder = json.load(open('./decodes/green_channel_decodes.json', 'r'))
blueChannelDecoder = json.load(open('./decodes/blue_channel_decodes.json', 'r'))

with open('ImageCompressed.txt', 'r') as fr:
    bit_stream = fr.read()

pixelStream = BitStreamDecoder.decoder(bit_stream, redChannelDecoder, greenChannelDecoder, blueChannelDecoder)

with open('ImageDecompressed.txt', 'w') as fr:
    fr.write(str(pixelStream))