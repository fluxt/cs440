import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import colorsys

img_width = 32
img_height = 32

def get_data(filename):
    lines = open(filename).readlines()

    image_arrs = []
    image_nums = []

    for img_num in range(len(lines) // (img_height + 1)):
        img_arr = []
        for i in range(img_height):
            line = lines[img_num * (img_height + 1) + i]
            img_arr.extend([ord(c) - 48 for c in line.strip()])
        line = lines[((img_num + 1) * (img_height + 1)) - 1]
        num = ord(line.strip()[0]) - 48

        image_arrs.append(img_arr)
        image_nums.append(num)

    return np.array(image_arrs), np.array(image_nums)

def get_test_data():
    return get_data("digitdata/optdigits-orig_test.txt")

def get_train_data():
    return get_data("digitdata/optdigits-orig_train.txt")

def write_image_to_file(filename, image):
    mpimg.imsave(filename, image.astype(float).reshape((img_width, img_height)), cmap='binary')
