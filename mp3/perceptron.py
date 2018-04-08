import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import utils
import random

num_digits = 10
img_width = 32
img_height = 32
init_weights_sd_dev = 10

img_folder = "images/"

num_epochs = 25
num_repeats = 20

def learning_rate_function(epoch_num):
    return 1 / (epoch_num + 1)

# adds a 1 to the end of each image in the list
def add_bias(images):
    return np.concatenate((images, np.array([[1] for n in range(images.shape[0])])), axis=1)

class PerceptionLearningRule:
    def __init__(self, train_images, train_numbers, b, rand_init_weights, rand_order):
        if np.size(train_images, 0) != np.size(train_numbers, 0):
            print("Error: image size does not match numbers size")
            return

        self.bias = b
        self.random_init_weights = rand_init_weights
        self.random_order = rand_order
        self.img_size = img_width * img_height
        if (bias):
            self.img_size += 1

        self.num_images = train_images.shape[0];

        if (bias):
            self.train_images = add_bias(train_images)
        else:
            self.train_images = train_images

        self.train_numbers = train_numbers

        if random_init_weights:
            # use a random distribution to initialize the weights
            self.weights = np.array([[np.random.randn() * init_weights_sd_dev for x  in range(self.img_size)] for y in range(num_digits)])
        else:
            self.weights = np.zeros((num_digits, self.img_size))

    # returns an array containing the value for each class (digits 0-9)
    def get_output(self, image):
        return np.array([np.dot(image, self.weights[i]) for i in range(num_digits)])

    # returns the perceptron's best guess for the provided image
    def get_guess(self, image):
        return np.argmax(self.get_output(image))

    # returns a tuple containing:
    #   - the accuracy of the perceptron over the set of images provided
    #   - the confusion matrix c, where c[i][j] is the proportion of the items in class i that were classified into class j by the perceptron
    def evaluate(self, test_images, test_numbers):
        if (bias):
            test_images = add_bias(test_images)

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

    # does one epoch of learning, with the specified learning rate
    def do_epoch(self, learning_rate):
        if self.random_order:
            order = [i for i in range(self.num_images)]
            random.shuffle(order)
        else:
            order = range(self.num_images)

        for i in order:
            image = self.train_images[i]

            guess = self.get_guess(image)
            real = self.train_numbers[i]

            # adjust the weights if the perceptron guessed wrong
            if (guess != real):
                self.weights[guess] -= image * learning_rate
                self.weights[real] += image * learning_rate

if __name__ == "__main__":
    # seed the random number generators
    random.seed(10)
    np.random.seed(10)

    train_images, train_numbers = utils.get_train_data()
    test_images, test_numbers = utils.get_test_data()

    # replace the zeros in the data with -1
    train_images[train_images == 0] = -1
    test_images[test_images == 0] = -1

    # stores the accuracies of each setup
    accuracies = np.zeros((8, num_epochs))
    # stores the labels each setup for the plot
    names = []

    for setup_num in range(8):
        bias = (setup_num & 4) == 0
        random_init_weights = (setup_num & 2) == 0
        random_order = (setup_num & 1) == 0

        # run num_repeat trials for each setup
        for repeat_num in range(num_repeats):
            classifier = PerceptionLearningRule(train_images, train_numbers, bias, random_init_weights, random_order)

            for epoch_num in range(num_epochs):
                accuracy, _ = classifier.evaluate(train_images, train_numbers)
                accuracies[setup_num][epoch_num] += accuracy

                classifier.do_epoch(learning_rate_function(epoch_num))

        name = ""
        if (bias):
            name += "Bias, "
        else:
            name += "No Bias, "

        if (random_init_weights):
            name += "Rnd. Init Wts, "
        else:
            name += "Wts Init to 0, "

        if (random_order):
            name += "Rnd. Order"
        else:
            name += "Set Order"
        names.append(name)
        print("Finished with: " + name)

    accuracies /= num_repeats

    # plot the accuracies of each of the setups
    for i in range(8):
        plt.plot(accuracies[i], label = names[i])
    plt.title("Perceptron Accuracy by Epoch")
    plt.xlabel("Epoch Number")
    plt.ylabel("Accuracy (Training Data)")
    plt.legend()
    plt.ylim((0, 1))
    plt.xlim((0, num_epochs - 1))
    plt.savefig(img_folder + "perceptron_accuracies.png")

    plt.clf()

    # plot the accuracies of each of te setups on a log scale
    for i in range(8):
        plt.plot(1 - accuracies[i], label = names[i])
    plt.title("Perceptron Accuracy by Epoch (Log scale)")
    plt.xlabel("Epoch Number")
    plt.ylabel("1 - Accuracy (Training Data)")
    plt.legend()
    plt.yscale('log', nonposy='clip')
    plt.xlim((0, num_epochs - 1))
    plt.savefig(img_folder + "perceptron_accuracies_log.png")

    # Run the perceptron once more to get the images of the weights, as well as the final accuracy and confusion matrix
    classifier = PerceptionLearningRule(train_images, train_numbers, False, True, True)
    for epoch_num in range(num_epochs):
        classifier.do_epoch(learning_rate_function(epoch_num))

    # create each of the
    for i in range(num_digits):
        utils.write_image_to_file_colored(img_folder + "weights_" + str(i) + ".png", classifier.weights[i])

    # get the accuracy and confusion matrix, based on the test images
    accuracy, confusion = classifier.evaluate(test_images, test_numbers)
    print("Accuracy: " + str(accuracy))
    print(np.around(confusion, 3))
