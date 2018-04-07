import numpy as np
import utils
import math
import random

num_digits = 10
img_width = 32
img_height = 32
img_size = img_width * img_height
#sklearn.metrics enables the use of confusion matrices. use confusion_matrix(x_act, x_predict)
#This solution of this matrix will output a numpy array

#sizes is the number of neurons in respective layers of network
class PerceptionLearningRule:
    def __init__(self, train_images, train_numbers):
        if np.size(train_images, 0) != np.size(train_numbers, 0):
            print("Error: image size does not match numbers size")
            return
        self.num_images = train_images.shape[0];
        #layers: number of neurons per layer in network
        #self.num_layers = len(sizes)
        #total size of neurons in layers of network
        #self.sizes = sizes

        #biases: initialized randomly utilizing a gaussian distribution
        self.train_images = train_images
        #self.images = np.concatenate((train_images, np.array([[1] for n in range(self.num_images)])), axis=1)

        self.train_numbers = train_numbers

        #weights: initialized randomly using gaussian dist. mean 0/var 1
        self.weights = np.array([[random.random() - .5 for x  in range(img_size)] for y in range(num_digits)])
        #self.weights = np.array([[random.random() - .5 for x  in range(img_size)] for y in range(num_digits)])

    def get_output(self, image):
        return np.array([np.dot(image, self.weights[i]) for i in range(num_digits)])

    def get_guess(self, image):
        return np.argmax(self.get_output(image))

    def evaluate(self, test_images, test_numbers):
        num_correct = 0
        confusion_matrix = np.zeros((num_digits, num_digits))

        for i in range(len(test_numbers)):
            guess = self.get_guess(test_images[i])
            if (guess == test_numbers[i]):
                num_correct += 1
            confusion_matrix[test_numbers[i]][guess] += 1

        for i in range(num_digits):
            confusion_matrix[i] /= np.sum(confusion_matrix[i])
        return (num_correct / len(test_numbers)), confusion_matrix

    def do_epoch(self, learning_rate = 0.001):
        order = [i for i in range(self.num_images)] # randomize?
        random.shuffle(order)
        for i in order:
            image = self.train_images[i]
            output = self.get_output(image)

            goal_output = np.zeros(num_digits)
            goal_output[self.train_numbers[i]] = 1

            self.weights += np.outer((goal_output - output), image) * learning_rate


if __name__ == "__main__":
    random.seed(10)

    train_images, train_numbers = utils.get_train_data()
    test_images, test_numbers = utils.get_test_data()

    classifier = PerceptionLearningRule(train_images, train_numbers)

    for i in range(150):
        accuracy, _ = classifier.evaluate(test_images, test_numbers)
        print("epoch " + str(i) + ": " + str(accuracy))
        classifier.do_epoch(learning_rate = 0.005 / ((i+1) ** .5))

    _, confusion = classifier.evaluate(test_images, test_numbers)
    print(np.around(confusion, 3))
