import utils
import game
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

learning_epochs = 1000

weight_scale = 0.01
learning_rate = .1
batch_size = 100
# number of inner layers for our neural network
num_layers = 3
# nourons per inner layer of our neural network
num_nodes_per_layer = 256

def affine_forward(A, W, b):
    return (A.dot(W)) + b

# also returns (A, W) for caching
def affine_forward_cache(A, W, b):
    return affine_forward(A, W, b), (A.copy(), W.copy())

# (A, W) passed in as 'cache'
# returns dA, dW, db
def affine_backward(dZ, cache):
    A, W = cache
    dA = dZ.dot(W.T)
    dW = (A.T).dot(dZ)
    db = np.sum(dZ, axis=0)
    return dA, dW, db

def ReLU_forward(Z):
    Z[Z < 0] = 0
    return Z

# also returns Z for caching
def ReLU_forward_cache(Z):
    cache = Z.copy()
    Z = ReLU_forward(Z)
    return Z, cache

# Z passed in as 'cache'
def ReLU_backward(dA, cache):
    Z = cache
    dA[Z < 0] = 0
    return dA

def cross_entropy(F, y):
    n = y.shape[0]
    L = 0
    dF = np.zeros(F.shape)
    for i in range(n):
        sum_exp_thing = np.sum(np.exp(F[i]))
        L += F[i][y[i]] - np.log(sum_exp_thing)

        expected = np.zeros(3)
        expected[y[i]] = 1
        dF[i] = expected - (np.exp(F[i]) / sum_exp_thing)
    L *= (-1 / n)
    dF *= (-1 / n)

    return L, dF

def action_num_to_action(act):
    if act == 0:
        return game.Action.UP
    elif act == 1:
        return game.Action.NOTHING
    elif act == 2:
        return game.Action.DOWN
    else:
        print("SOMETHING IS WRONG!!!")

class Deep_Learner:
    def normalize(self, states):
        return (states - self.means) / self.std_deviations

    # layers is the number of inner layers
    def __init__(self, training_states, training_actions, layers, nodes_per_layer):
        # set the means and standard deviations for normalizing the states
        self.means = np.mean(training_states, axis=0)
        self.std_deviations = np.std(training_states, axis=0)

        self.train_states = self.normalize(training_states)
        self.train_actions = training_actions

        self.layers = layers

        # set up the weight matrix for each layer
        self.W = [0 for i in range(layers + 1)]
        self.W[0] = np.random.uniform(0, weight_scale, size=(5, nodes_per_layer))
        for i in range(1, layers):
            self.W[i] = np.random.uniform(0, weight_scale, size=(nodes_per_layer, nodes_per_layer))
        self.W[layers] = np.random.uniform(0, weight_scale, size=(nodes_per_layer, 3))

        # set up the bias vectors for each layer
        self.b = [0 for i in range(layers + 1)]
        for i in range(layers):
            self.b[i] = np.zeros(nodes_per_layer)
        self.b[layers] = np.zeros(3)

    # train the network on a batch of inputs
    # X = batch_states, y=batch_actions
    def do_minibatch(self, batch_states, batch_actions):
        # forward propogation
        acache = [0 for n in range(self.layers + 1)]
        rcache = [0 for n in range(self.layers)]
        A = batch_states

        for layer_num in range(self.layers):
            Z, acache[layer_num] = affine_forward_cache(A, self.W[layer_num], self.b[layer_num])
            A, rcache[layer_num] = ReLU_forward_cache(Z)
        F, acache[self.layers] = affine_forward_cache(A, self.W[self.layers], self.b[self.layers])

        loss, dF = cross_entropy(F, batch_actions)

        # back-propogation
        dW = [0 for n in range(self.layers + 1)]
        db = [0 for n in range(self.layers + 1)]

        dA, dW[self.layers], db[self.layers] = affine_backward(dF, acache[self.layers])
        for layer_num in range(self.layers - 1, -1, -1):
            dZ = ReLU_backward(dA, rcache[layer_num])
            dA, dW[layer_num], db[layer_num] = affine_backward(dZ, acache[layer_num])

        # gradient descent
        for i in range(self.layers + 1):
            self.W[i] -= learning_rate * dW[i]
            self.b[i] -= learning_rate * db[i]
        return loss

    # get the network's output vector for a given input
    def get_action_num(self, inputs):
        inputs = self.normalize(inputs)
        A = inputs
        for layer_num in range(self.layers):
            Z = affine_forward(A, self.W[layer_num], self.b[layer_num])
            A = ReLU_forward(Z)
        F = affine_forward(A, self.W[self.layers], self.b[self.layers])
        return np.argmax(F)

    def get_action(self, state):
        return action_num_to_action(self.get_action_num(state))

    # do an entire epoch of learning
    # returns the sum of the losses for each batch
    def do_epoch(self):
        # get a random order to put the data in
        order = np.arange(len(self.train_actions))
        np.random.shuffle(order)
        total_loss = 0

        for batch_num in range(len(self.train_actions) // batch_size):
            batch_states = np.array([self.train_states[order[i]] for i in range(batch_num * batch_size, min(len(self.train_actions), ((batch_num+1) * batch_size) - 1))])
            batch_actions = np.array([self.train_actions[order[i]] for i in range(batch_num * batch_size, min(len(self.train_actions), ((batch_num+1) * batch_size) - 1))])

            total_loss += self.do_minibatch(batch_states, batch_actions)
        return total_loss

if __name__ == "__main__":
    np.random.seed(24)

    states, actions = utils.get_data()
    learner = Deep_Learner(states, actions, num_layers, num_nodes_per_layer)

    loss_arr = np.zeros(learning_epochs)
    for i in range(learning_epochs):
        loss = learner.do_epoch()
        print("i = " + str(i) + ", loss = " + str(loss))
        loss_arr[i] = loss

    plt.plot(loss_arr)
    plt.title("Deep Learning: Loss by Epoch")
    plt.ylabel("Total Loss")
    plt.xlabel("Epoch Number")
    plt.xlim((0, learning_epochs))
    plt.ylim((0, max(loss_arr)))
    plt.savefig("image/deep_plot.png")

    correct = 0
    for i in range(len(actions)):
        if learner.get_action_num(states[i]) == actions[i]:
            correct += 1
    print(correct)
    print(len(actions))
