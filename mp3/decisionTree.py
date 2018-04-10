import numpy as np
from sklearn import tree
import utils

X, Y = utils.get_train_data()

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)

test_images, test_labels = utils.get_test_data()

num_correct = 0
confusion_matrix = np.zeros((10, 10))
guesses = clf.predict(test_images)
for i in range(len(test_images)):
    guess = guesses[i]
    real = test_labels[i]

    if guess == real:
        num_correct += 1

    confusion_matrix[real][guess] += 1

for i in range(10):
    confusion_matrix[i] /= np.sum(confusion_matrix[i])
accuracy = num_correct / len(test_labels)

print("Accuracy: " + str(accuracy))
print(np.around(confusion_matrix, 3))
