import numpy as np
import utils
import math

num_digits = 2
img_width = 60
img_height = 70

class SinglePixelClassifier:
    # constructor. perform training here
    def __init__(self, train_images, train_numbers, laplace_smoothing = 1.0):
        # return error if image size does not match numbers size
        if np.size(train_images, 0) != np.size(train_numbers, 0):
            print("Error: image size does not match numbers size")
            return

        # laplace smoothing is 6 unless you specify otherwise
        self.laplace_smoothing = laplace_smoothing

        # performing training here we count the number of blacks and whites, and number of the features
        self.size = train_numbers.size
        self.black_count = np.zeros((num_digits, img_width*img_height))
        self.white_count = np.zeros((num_digits, img_width*img_height))
        self.digit_count = np.bincount(train_numbers)
        for i in range(self.size):
            self.black_count[train_numbers[i]] += train_images[i]
            self.white_count[train_numbers[i]] += np.logical_not(train_images[i])

    # classifier. pass image to check which one you get
    def classify(self, test_image):
        probabilities = np.zeros((num_digits))
        for digit in range(num_digits):
            probabilities[digit] = np.log(self.digit_count[digit]/self.size)
            for index in range(img_width*img_height):
                if test_image[index] == 1:
                    probabilities[digit] += np.log((self.black_count[digit][index] + self.laplace_smoothing) / (self.digit_count[digit] + 2 * self.laplace_smoothing))
                else:
                    probabilities[digit] += np.log((self.white_count[digit][index] + self.laplace_smoothing) / (self.digit_count[digit] + 2 * self.laplace_smoothing))

        # output the digit with the highest posterior probability
        output = np.argmax(probabilities)
        return output, probabilities

    def evaluate(self, test_images, test_numbers):
        if np.size(test_images, 0) != np.size(test_numbers, 0):
            print("Error: image size does not match numbers size")
            return 0.0

        accuracy = 0.0
        confusion_matrix = np.zeros((num_digits, num_digits))
        for i in range(test_numbers.size):
            # get output based on test images
            output, _ = self.classify(test_images[i])

            # update accuracy, confusion matrix, most_prototytpical, and least_prototypical
            truth_label = test_numbers[i]
            if output == truth_label:
                accuracy += 1
            confusion_matrix[truth_label][output] += 1

        accuracy /= test_numbers.size

        for i in range(num_digits):
            confusion_matrix[i] = confusion_matrix[i] / np.sum(confusion_matrix[i])

        return accuracy, confusion_matrix

if __name__ == "__main__":
    train_images, train_numbers = utils.get_face_train_data()
    test_images, test_numbers = utils.get_face_test_data()

    # train here
    classifier = SinglePixelClassifier(train_images, train_numbers)

    # classify here
    accuracy, confusion_matrix = classifier.evaluate(test_images, test_numbers)

    print("\nAccuracy over all of test data: {:.2%}".format(accuracy))

    print("\nConfusion matrix: row - truth label, column - classifier output")
    print(np.around(confusion_matrix, 3))
