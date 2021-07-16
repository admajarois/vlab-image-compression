import numpy as np

def histogram_array_generator(image):
    histogram_array = {}
    for index in range(256):
        histogram_array[index] = 0
    for row in image:
        for element in row:
            histogram_array[element] += 1
    return histogram_array

def probability_distribution_generator(array, image_dimension):
    prob_dist_array = {}
    for index in range(256):
        prob_dist_array[index] = array[index]/image_dimension
    return prob_dist_array

def pixel_frequency(list):
    pixel_number={}
    for i in list:
        if i not in pixel_number.keys():
            pixel_number[i]=1
        else:
            pixel_number[i]+=1
    return pixel_number

def pixel_probability(pixel, image_dimension):
    prob_pixel_array = {}
    for i in pixel.keys():
        prob_pixel_array[i] = round(pixel[i]/image_dimension, 2)
    return prob_pixel_array
    
