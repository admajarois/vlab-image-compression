from huffman import HuffmanCoding
import sys
import cv2

# path = "sample.txt"

# h = HuffmanCoding(path)

# output_path = h.compress()
# print(output_path)

img = cv2.imread('mosaic_monalisa.jpg')

dimension = img.shape

height = img.shape[0]
width = img.shape[1]

print(height ," X ", width)