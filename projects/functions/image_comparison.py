from skimage.metrics import structural_similarity as ssim
import numpy as np
import cv2

def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    return err

def compare_images(imageA, imageB):
    original_image = cv2.imread(imageA)
    compressed_image = cv2.imread(imageB)

    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    compressed_image = cv2.cvtColor(compressed_image, cv2.COLOR_BGR2GRAY)

    m = mse(original_image, compressed_image)
    s = ssim(original_image, compressed_image)

    return m,s