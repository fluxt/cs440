import numpy as np
import utils
import math

num_digits = 10
img_width = 32
img_height = 32

class SinglePixelClassifier:
    def __init__(self, train_images, train_numbers, laplace_smoothing = 6.0):
        if np.size(train_images, 0) != np.size(train_numbers, 0):
            print("Error: image size does not match numbers size")
            return

        self.laplace_smoothing = laplace_smoothing
        self.size = train_numbers.size
        self.black_count = np.zeros((num_digits, img_width*img_height), dtype=int)
        self.digit_count = np.bincount(train_numbers)
        for i in range(self.size):
            self.black_count[train_numbers[i]] += train_images[i]

    def get_priors(self, index, digit, feature):
        black_prior = ( self.black_count[digit][index] + self.laplace_smoothing ) / ( self.digit_count[digit] + 2*self.laplace_smoothing )
        if feature == 1:
            return black_prior
        else:
            return 1-black_prior

    def classify(self, test_image):
        probabilities = np.zeros((num_digits), dtype=float)
        for digit in range(num_digits):
            digit_prob = math.log(self.digit_count[digit]/self.size)
            for index in range(img_width*img_height):
                digit_prob += math.log(self.get_priors(index, digit, test_image[index]))
            probabilities[digit] = digit_prob

        output = np.argmax(probabilities)
        return output, probabilities

    def evaluate(self, test_images, test_numbers):
        if np.size(test_images, 0) != np.size(test_numbers, 0):
            print("Error: image size does not match numbers size")
            return

        accuracy = 0
        for i in range(test_numbers.size):
            output, _ = self.classify(test_images[i])
            if output == test_numbers[i]:
                accuracy += 1

        accuracy /= test_numbers.size

        return accuracy

if __name__ == "__main__":
    train_images, train_numbers = utils.get_train_data()
    test_images, test_numbers = utils.get_test_data()

    classifier = SinglePixelClassifier(train_images, train_numbers)
    print("Evaluating...")
    accuracy = classifier.evaluate(test_images, test_numbers)
    print("Accuracy over all of test data: {:.2%}".format(accuracy))
