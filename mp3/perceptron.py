import numpy as np
from sklearn.metrics import confusion_matrix
import utils
import math
import random

num_digits = 10
img_width = 32
img_height = 32
#sklearn.metrics enables the use of confusion matrices. use confusion_matrix(x_act, x_predict)
#This solution of this matrix will output a numpy array

#sizes is the number of neurons in respective layers of network
class PerceptionLearningRule:
    def __init__(self, train_images, train_numbers, sizes):
        if np.size(train_images, 0) != np.size(train_numbers, 0):
            print("Error: image size does not match numbers size")
            return
        #layers: number of neurons per layer in network
        self.num_layers = len(sizes)
        #total size of neurons in layers of network
        self.sizes = sizes
        #biases: initialized randomly utilizing a gaussian distribution
        self.biases = [np.random.randn(x, 1) for x in sizes[1:]]
        #weights: initialized randomly using gaussian dist. mean 0/var 1
        self.weights = [np.random.randn(x,y) for x, y in zip(sizes[:-1], sizes[1:])]

    #function to return network output with input i
    def forwardfeed(self, i):
        #need more stuff
        return i

    #funciton to train the network to learn.
    def StochasticGradientDec(self, train_data, num_epochs, batch_size,learning_rate,test_data = none):
        #train using decending StochasticGradientDec
        #need to use a potential helper function to propagate backwards


if __name__ == "__main__":
    train_images, train_numbers = utils.get_train_data()
    test_images, test_numbers = utils.get_test_data()

    classifier = SinglePixelClassifier(train_images, train_numbers)
    print("Evaluating...")
    accuracy = classifier.evaluate(test_images, test_numbers)
    print("Accuracy over all of test data: {:.2%}".format(accuracy))
