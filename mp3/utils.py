import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

img_width = 32
img_height = 32

face_width = 60
face_height = 70

def face_char_to_num(ch):
    if ch == '#':
        return 1
    elif ch == ' ':
        return 0
    else:
        return float('inf')

def get_face_data(data_file, labels_file):
    image_data = open(data_file).readlines()
    labels_data = open(data_file).readlines()

    image_arrs = []
    labels = []

    for img_num in range(len(image_data) // face_height):
        img_arr = []
        for i in range(face_height):
            line = lines[img_num * (face_height)]
            img_arr.extend([face_char_to_num(c) for c in image_data.strip()])
        line = image_data[((img_num + 1) * face_height) - 1]

        img_arrs.append(img_arr)
        image_datas.append(ord(labels_data[img_num]) - 48)
    return np.array(image_arrs), np.array(labels)

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

def get_face_test_data():
    return get_face_data("facedata/facedatatest.txt", "facedata/facedatatestlabels.txt")

def get_face_train_data():
    return get_face_data("facedata/facedatatrain.txt", "facedata/facedatatrainlabels.txt")

def write_image_to_file(filename, image):
    mpimg.imsave(filename, image.astype(float).reshape((img_width, img_height)), cmap='binary')

def write_image_to_file_colored(filename, image):
    plt.imsave(filename, image.astype(float).reshape((img_width, img_height)), cmap="jet")

def write_image_to_file_colored_with_bar(filename, image):
    plt.imshow(image.astype(float).reshape((img_width, img_height)), cmap="jet")
    plt.colorbar()
    plt.savefig(filename)
    plt.clf()
