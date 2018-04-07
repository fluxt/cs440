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
            return 0.0

        accuracy = 0.0
        confusion_matrix_accumulator = np.zeros((num_digits, num_digits), dtype=int)
        confusion_matrix = np.zeros((num_digits, num_digits), dtype=float)
        self.most_prototypical = [ (0, float("-Inf"), 0, 0) ] * num_digits
        self.least_prototypical = [ (0, float("Inf"), 0, 0) ] * num_digits
        for i in range(test_numbers.size):
            output, posterior_probabilities = self.classify(test_images[i])

            # update accuracy, confusion matrix, most_prototytpical, and least_prototypical
            truth_label = test_numbers[i]
            posterior_probability = posterior_probabilities[output]
            if output == truth_label:
                accuracy += 1
            confusion_matrix_accumulator[truth_label][output] += 1
            if (posterior_probability > self.most_prototypical[truth_label][1]):
                self.most_prototypical[truth_label] = (i, posterior_probability, truth_label, output)
            if (posterior_probability < self.least_prototypical[truth_label][1]):
                self.least_prototypical[truth_label] = (i, posterior_probability, truth_label, output)

        accuracy /= test_numbers.size

        for i in range(num_digits):
            confusion_matrix[i] = confusion_matrix_accumulator[i] / np.sum(confusion_matrix_accumulator[i])

        return accuracy, confusion_matrix

    def get_prototypical(self):
        return self.most_prototypical, self.least_prototypical

    def get_odds_ratio(self, images, numbers):
        # count = np.zeros((num_digits, img_width*img_height), dtype=int)
        return

if __name__ == "__main__":
    np.set_printoptions(threshold=np.nan)

    train_images, train_numbers = utils.get_train_data()
    test_images, test_numbers = utils.get_test_data()

    classifier = SinglePixelClassifier(train_images, train_numbers)

    accuracy, confusion_matrix = classifier.evaluate(test_images, test_numbers)

    print("\nAccuracy over all of test data: {:.2%}".format(accuracy))

    print("\nConfusion matrix:")
    print(np.around(confusion_matrix, 3))

    most_prototypical, least_prototypical = classifier.get_prototypical()

    print("\nMost Prototypical:")
    for i in range(num_digits):
        print(most_prototypical[i])
        utils.write_image_to_file("most-prototytpical"+str(i)+".png", test_images[most_prototypical[i][0]])

    print("\nLeast Prototypical:")
    for i in range(num_digits):
        print(least_prototypical[i])
        utils.write_image_to_file("least-prototytpical"+str(i)+".png", test_images[least_prototypical[i][0]])
