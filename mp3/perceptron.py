import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import utils
import math
import random

bias = False
random_init_weights = False
random_order = False

num_digits = 10
img_width = 32
img_height = 32

#sklearn.metrics enables the use of confusion matrices. use confusion_matrix(x_act, x_predict)
#This solution of this matrix will output a numpy array

#sizes is the number of neurons in respective layers of network
class PerceptionLearningRule:
    def __init__(self, train_images, train_numbers):
        if np.size(train_images, 0) != np.size(train_numbers, 0):
            print("Error: image size does not match numbers size")
            return
        self.img_size = img_width * img_height
        if (bias):
            self.img_size += 1

        self.num_images = train_images.shape[0];
        #layers: number of neurons per layer in network
        #self.num_layers = len(sizes)
        #total size of neurons in layers of network
        #self.sizes = sizes

        #biases: initialized randomly utilizing a gaussian distribution
        self.train_images = train_images

        self.train_numbers = train_numbers

        #weights: initialized randomly using gaussian dist. mean 0/var 1
        if random_init_weights:
            self.weights = np.array([[random.random() - .5 for x  in range(self.img_size)] for y in range(num_digits)])
        else:
            self.weights = np.zeros((num_digits, self.img_size))

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
        if random_order:
            order = [i for i in range(self.num_images)]
            random.shuffle(order)
        else:
            order = range(self.num_images)

        for i in order:
            image = self.train_images[i]

            guess = self.get_guess(image)
            real = self.train_numbers[i]

            if (guess != real):
                self.weights[guess] -= image * learning_rate
                self.weights[real] += image * learning_rate

def add_bias(images):
    return np.concatenate((images, np.array([[1] for n in range(images.shape[0])])), axis=1)

if __name__ == "__main__":

    no_bias_train, train_numbers = utils.get_train_data()
    no_bias_test, test_numbers = utils.get_test_data()

    bias_train = add_bias(no_bias_train)
    bias_test = add_bias(no_bias_test)

    for i in range(8):
        bias = (i & 4) == 0
        #print("bias = " + str(bias))
        random_init_weights = (i & 2) == 0
        #print("random_init_weights = " + str(random_init_weights))
        random_order = (i & 1) == 0
        #print("random_order = " + str(random_order))

        random.seed(10)

        if (bias):
            train_images = bias_train
            test_images = bias_test
        else:
            train_images = no_bias_train
            test_images = no_bias_test

        classifier = PerceptionLearningRule(train_images, train_numbers)

        accuracies = []
        for i in range(20):
            accuracy, _ = classifier.evaluate(test_images, test_numbers)
            accuracies.append(accuracy)
            #print("epoch " + str(i) + ": " + str(accuracy))

            classifier.do_epoch(learning_rate = 1 / ((i+1) ** 0.5))

        name = ""
        if (bias):
            name += "Bias, "
        else:
            name += "No Bias, "

        if (random_init_weights):
            name += "Rand. Init Weights, "
        else:
            name += "Weights Init to 0, "

        if (random_order):
            name += "Rnd. Training Order"
        else:
            name += "Set Training Order"

        plt.plot(accuracies, label = name)

    plt.title("Perceptron Accuracy by Epoch")
    plt.xlabel("Epoch Number")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.savefig("perceptron_accuracies.png")
    plt.title("Perceptron Accuracy by Epoch (Zoom)")
    plt.ylim((0.85, 1))
    plt.savefig("perceptron_accuracies_zoom.png")

    _, confusion = classifier.evaluate(test_images, test_numbers)
    #print(np.around(confusion, 3))
