import utils
import game
import numpy as np

learning_rate = 0.3
batch_size = 100
num_layers = 4
num_nodes_per_layer = 100

class Deep_Learner:
    def __init__(self, training_states, training_actions, activation_function, layers, nodes_per_layer):
        self.train_states = training_states
        self.train_actions = training_actions
        self.activation_function = activation_function

        self.W = np.zeros((layers-1, nodes_per_layer, nodes_per_layer))
        self.W_in = np.zeros((nodes_per_layer, 5))
        self.W_out = np.zeros((3, nodes_per_layer))
        self.b = np.zeros((layers, nodes_per_layer))


    def do_minibatch(self, batch_states, batch_actions):


    def do_epoch(self):
        order = np.arange(len(self.train_states))
        np.random.shuffle(order)

        for batch_num in range(len(self.train_states) // batch_size):
            batch_states = []
            batch_actions = []
            for i in range(batch_num * batch_size, min(len(self.train_states), ((batch_num+1) * batch_size) - 1)):
                batch_states.append(self.train_states[order[i]])
                batch_actions.append(self.train_actions[order[i]])
            batch_states = np.array(batch_states)

            self.do_minibatch(batch_states, batch_actions)


def affine_forward(a, w, b):
    assert a.ndim == 2 and w.ndim == 2 and b.ndim = 1
    a_row, a_col = a.shape()
    w_row, w_col = w.shape()
    b_num = b.shape()
    assert a_row > 0 and a_col > 0 and w_row > 0 and w_col > 0 and b_num > 0
    assert a_col == w_row
    assert w_col == b_num
    # n = a_row
    # d = a_col
    # dp = w_col
    z = np.zeros((a_row, w_col)) # n x dp
    for i in range(a_row): # n
        for j in range(w_col): # dp
            z[i][j] = np.dot(a[i,:] * w[:,j]) + b[j]
    a_cache = np.copy(a)
    w_cache = np.copy(w)
    b_cache = np.copy(b)
    return z, (a_cache, w_cache, b_cache)

def affine_backward(dz, cache):
    pass

def ReLU_forward(z):
    pass

def ReLU_backward(z):
    pass

def cross_entrophy(f, y):
    pass

def ReLU(x):
    return max(x, 0)

if __name__ == "__main__":
    np.random.seed(24)

    states, actions = utils.get_data()
    learner = Deep_Learner(states, actions, ReLU)

    for i in range(1):
        learner.do_epoch()
