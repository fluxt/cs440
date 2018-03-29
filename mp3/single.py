import numpy as np
import utils

number_size = 10
img_width = 32
img_height = 32

class SinglePixelFeatures:
    def __init__(self, images, numbers):
        if np.size(images, 0) != np.size(numbers, 0):
            print("Error: image size does not match numbers size")
            return

        self.size = numbers.size
        self.count = np.zeros((number_size, img_width*img_height), dtype=int)
        for i in range(self.size):
            self.count[numbers[i]] += images[i]

if __name__ == "__main__":
    images, numbers = utils.get_train_data()
    single_pixel = SinglePixelFeatures(images, numbers)
    np.set_printoptions(threshold=np.inf)
    print(single_pixel.count[7].reshape(32,32))
    