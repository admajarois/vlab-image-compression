import cv2
import numpy as np
import os
from flask_login import current_user

from projects.functions import channel_restorer

def restorer(image):
    result = os.path.join("projects/results", current_user.NIM)
    with open(result+'/image_pixel_stream.txt', 'r') as fr:
        pixel_stream = fr.read()

    pixel_stream = pixel_stream.replace('[', '')
    pixel_stream = pixel_stream.replace(']', '')
    pixel_stream = pixel_stream.split(', ')
    pixel_stream = [int(pixel) for pixel in pixel_stream]
 
    red_channel_pixel_stream = pixel_stream[:int(len(pixel_stream)/3)]
    green_channel_pixel_stream = pixel_stream[int(len(pixel_stream)/3):int((2*len(pixel_stream))/3)]
    blue_channel_pixel_stream = pixel_stream[int((2*len(pixel_stream))/3):int(len(pixel_stream))]
    
    original_image = cv2.imread(image)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    
    red_channel_image = np.reshape(red_channel_pixel_stream, (original_image.shape[0], original_image.shape[1]))
    green_channel_image = np.reshape(green_channel_pixel_stream, (original_image.shape[0], original_image.shape[1]))
    blue_channel_image = np.reshape(blue_channel_pixel_stream, (original_image.shape[0], original_image.shape[1]))

    red_channel_loss = original_image[:,:,0] - red_channel_image
    green_channel_loss = original_image[:,:,1] - green_channel_image
    blue_channel_loss = original_image[:,:,2] - blue_channel_image

    total_loss = np.sum(red_channel_loss) + np.sum(green_channel_loss) + np.sum(blue_channel_loss)
    restored_image = channel_restorer.image_restorer(red_channel_image, green_channel_image, blue_channel_image)
    original_image_dimension = np.array(original_image).shape
    restore_image_dimension = np.array(restored_image).shape

    return total_loss, original_image_dimension, restore_image_dimension

def gray_restorer(image):
    result = os.path.join("projects/results", current_user.NIM)
    with open(result+'/gray_image_pixel_stream.txt', 'r') as fr:
        gray_pixel_stream = fr.read()
    gray_pixel_stream = gray_pixel_stream.replace('[', '')
    gray_pixel_stream = gray_pixel_stream.replace(']', '')
    gray_pixel_stream = gray_pixel_stream.split(', ')
    gray_pixel_stream = [int(pixel) for pixel in gray_pixel_stream]
  
    original_image = cv2.imread(image)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    gray_channel_image = np.reshape(gray_pixel_stream, (original_image.shape[0], original_image.shape[1]))

    print(gray_channel_image)



    # print(len(gray_pixel_stream))

    # print(merged)

    
    # image_reshape = np.reshape(gray_pixel_stream, (original_image[0], original_image[1], 3))
    result_image = cv2.imwrite('./image_restore_gray.jpg', gray_channel_image)
  

    



# image = './uploads/stones.jpg'
# restorer = restorer(image)

# print(restorer)

