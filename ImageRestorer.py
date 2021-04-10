import cv2
import numpy as np

from functions import ChannelRestorer

with open('ImageDecompressed.txt', 'r') as fr:
    pixelStream = fr.read()

pixelStream = pixelStream.replace('[', '')
pixelStream = pixelStream.replace(']', '')
pixelStream = pixelStream.split(', ')
pixelStream = [int(pixel) for pixel in pixelStream]

redChannelPixelStream = pixelStream[:int(len(pixelStream)/3)]
greenChannelPixelStream = pixelStream[int(len(pixelStream)/3):int((2*len(pixelStream))/3)]
blueChannelPixelStream = pixelStream[int((2*len(pixelStream))/3):int(len(pixelStream))]

print(len(redChannelPixelStream))
print(len(pixelStream))

originalImage = cv2.imread('image.jpg')
originalImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB)

redChannelImage = np.reshape(redChannelPixelStream, (originalImage.shape[0], originalImage.shape[1]))
greenChannelImage = np.reshape(greenChannelPixelStream, (originalImage.shape[0], originalImage.shape[1]))
blueChannelImage = np.reshape(blueChannelPixelStream, (originalImage.shape[0], originalImage.shape[1]))

# print(greenChannelImage)

# redChannelLoss = originalImage[:,:,0] - redChannelImage
# greenChannelLoss = originalImage[:,:,1] - greenChannelImage
# blueChannelLoss = originalImage[:,:,2] - blueChannelImage

# totalLoss = np.sum(redChannelLoss) + np.sum(greenChannelLoss) + np.sum(blueChannelLoss)
# print("Total loss (across all red, green, blue channels : ", totalLoss )

# restoredImage = ChannelRestorer.imageRestorer(redChannelImage, greenChannelImage, blueChannelImage)

# print("Original image dimension: ", np.array(original_image).shape)
# print("Restored image dimension: ", np.array(restored_image).shape)