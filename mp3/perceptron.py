import numpy as np
from sklearn.metrics import confusion_matrix
import utils
import math

num_digits = 10
img_width = 32
img_height = 32
#sklearn.metrics enables the use of confusion matrices. use confusion_matrix(x_act, x_predict)
#This solution of this matrix will output a numpy array

class PerceptionLearningRule:
    def __init__(self, train_images, train_numbers):
        if np.size(train_images, 0) != np.size(train_numbers, 0):
            print("Error: image size does not match numbers size")
            return






if __name__ == "__main__":
    train_images, train_numbers = utils.get_train_data()
    test_images, test_numbers = utils.get_test_data()

    classifier = SinglePixelClassifier(train_images, train_numbers)
    print("Evaluating...")
    accuracy = classifier.evaluate(test_images, test_numbers)
    print("Accuracy over all of test data: {:.2%}".format(accuracy))
