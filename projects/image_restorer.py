import cv2
import numpy as np

from projects.functions import channel_restorer

def restorer(image):
    with open('projects/image_pixel_stream.txt', 'r') as fr:
        pixel_stream = fr.read()

    pixel_stream = pixel_stream.replace('[', '')
    pixel_stream = pixel_stream.replace(']', '')
    pixel_stream = pixel_stream.split(', ')
    pixel_stream = [int(pixel) for pixel in pixel_stream]

    red_channel_pixel_stream = pixel_stream[:int(len(pixel_stream)/3)]
    green_channel_pixel_stream = pixel_stream[int(len(pixel_stream)/3):int((2*len(pixel_stream))/3)]
    blue_channel_pixel_stream = pixel_stream[int((2*len(pixel_stream))/3):int(len(pixel_stream))]

    original_image =cv2.imread(image)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    red_channel_image = np.reshape(red_channel_pixel_stream, (original_image.shape[0], original_image[1]))
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


# image = './uploads/stones.jpg'
# restorer = restorer(image)

# print(restorer)

