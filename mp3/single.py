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
        self.black_count = np.zeros((num_digits, img_width*img_height))
        self.white_count = np.zeros((num_digits, img_width*img_height))
        self.digit_count = np.bincount(train_numbers)
        for i in range(self.size):
            self.black_count[train_numbers[i]] += train_images[i]
            self.white_count[train_numbers[i]] += np.logical_not(train_images[i])

    def classify(self, test_image):
        probabilities = np.zeros((num_digits))
        for digit in range(num_digits):
            probabilities[digit] = np.log(self.digit_count[digit]/self.size)
            for index in range(img_width*img_height):
                if test_image[index] == 1:
                    probabilities[digit] += np.log((self.black_count[digit][index] + self.laplace_smoothing) / (self.digit_count[digit] + 2 * self.laplace_smoothing))
                else:
                    probabilities[digit] += np.log((self.white_count[digit][index] + self.laplace_smoothing) / (self.digit_count[digit] + 2 * self.laplace_smoothing))

        # print(probabilities)
        output = np.argmax(probabilities)
        return output, probabilities

    def evaluate(self, test_images, test_numbers):
        if np.size(test_images, 0) != np.size(test_numbers, 0):
            print("Error: image size does not match numbers size")
            return 0.0

        accuracy = 0.0
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
            confusion_matrix[truth_label][output] += 1
            if (posterior_probability > self.most_prototypical[truth_label][1]):
                self.most_prototypical[truth_label] = (i, posterior_probability, truth_label, output)
            if (posterior_probability < self.least_prototypical[truth_label][1]):
                self.least_prototypical[truth_label] = (i, posterior_probability, truth_label, output)

        accuracy /= test_numbers.size

        for i in range(num_digits):
            confusion_matrix[i] = confusion_matrix[i] / np.sum(confusion_matrix[i])

        return accuracy, confusion_matrix

    def get_prototypical(self):
        return self.most_prototypical, self.least_prototypical

    def get_odds_ratio(self, a, b):
        a_map = (self.black_count[a] + self.laplace_smoothing) / (self.digit_count[a] + 2.0 * self.laplace_smoothing)
        b_map = (self.black_count[b] + self.laplace_smoothing) / (self.digit_count[b] + 2.0 * self.laplace_smoothing)
        odds_map = a_map / b_map
        return np.log(a_map), np.log(b_map), np.log(odds_map)

if __name__ == "__main__":
    np.set_printoptions(threshold=np.nan)

    train_images, train_numbers = utils.get_train_data()
    test_images, test_numbers = utils.get_test_data()

    classifier = SinglePixelClassifier(train_images, train_numbers)

    accuracy, confusion_matrix = classifier.evaluate(test_images, test_numbers)

    print("\nAccuracy over all of test data: {:.2%}".format(accuracy))

    print("\nConfusion matrix: row - truth label, column - classifier output")
    print(np.around(confusion_matrix, 3))

    most_prototypical, least_prototypical = classifier.get_prototypical()

    print("\nMost Prototypical: (index, prior, truth label, classifier output)")
    for i in range(num_digits):
        print(most_prototypical[i])
        utils.write_image_to_file("most-prototytpical"+str(i)+".png", test_images[most_prototypical[i][0]])

    print("\nLeast Prototypical: (index, prior, truth label, classifier output)")
    for i in range(num_digits):
        print(least_prototypical[i])
        utils.write_image_to_file("least-prototytpical"+str(i)+".png", test_images[least_prototypical[i][0]])

    print("\nPrinting Odds Ratio...")
    a_map, b_map, odds_map = classifier.get_odds_ratio(2, 8)
    utils.write_image_to_file_colored("2-map.png", a_map)
    utils.write_image_to_file_colored("8-map.png", b_map)
    utils.write_image_to_file_colored("odds-map-2-8.png", odds_map)

    a_map, b_map, odds_map = classifier.get_odds_ratio(4, 7)
    utils.write_image_to_file_colored("4-map.png", a_map)
    utils.write_image_to_file_colored("7-map.png", b_map)
    utils.write_image_to_file_colored("odds-map-4-7.png", odds_map)

    a_map, b_map, odds_map = classifier.get_odds_ratio(5, 9)
    utils.write_image_to_file_colored("5-map.png", a_map)
    utils.write_image_to_file_colored("9-map.png", b_map)
    utils.write_image_to_file_colored("odds-map-5-9.png", odds_map)

    a_map, b_map, odds_map = classifier.get_odds_ratio(9, 7)
    utils.write_image_to_file_colored("9-map.png", a_map)
    utils.write_image_to_file_colored("7-map.png", b_map)
    utils.write_image_to_file_colored("odds-map-9-7.png", odds_map)
