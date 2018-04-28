import utils
import game
import numpy as np

learning_epochs = 500

weight_scale = 0.01
learning_rate = .1
batch_size = 100
num_layers = 3
num_nodes_per_layer = 256

# also returns (A, W, b) for caching
def affine_forward(A, W, b):
    return ((A.dot(W)) + b), (A.copy(), W.copy(), b.copy())

# (A, W, b) passed in as 'cache'
# returns dA, dW, db
def affine_backward(dZ, cache):
    A, W, b = cache
    dA = dZ.dot(W.T)
    dW = (A.T).dot(dZ)
    db = np.sum(dZ, axis=0)
    return dA, dW, db


# also returns Z for caching
def ReLU_forward(Z):
    cache = Z.copy()
    Z[Z < 0] = 0
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
        return game.Action.DOWN
    elif act == 1:
        return game.Action.NOTHING
    elif act == 2:
        return game.Action.UP
    else:
        print("SOMETHING IS WRONG!!!")

class Deep_Learner:
    def normalize(self, states):
        return (states - self.means) / self.std_deviations

    # layers is the number of inner layers
    def __init__(self, training_states, training_actions, layers, nodes_per_layer):
        self.means = np.mean(training_states, axis=0)
        self.std_deviations = np.std(training_states, axis=0)

        self.train_states = self.normalize(training_states)
        self.train_actions = training_actions

        self.layers = layers
        self.W = [0 for i in range(layers + 1)]
        self.W[0] = np.random.uniform(0, weight_scale, size=(5, nodes_per_layer))
        for i in range(1, layers):
            self.W[i] = np.random.uniform(0, weight_scale, size=(nodes_per_layer, nodes_per_layer))
        self.W[layers] = np.random.uniform(0, weight_scale, size=(nodes_per_layer, 3))

        self.b = [0 for i in range(layers + 1)]
        for i in range(layers):
            self.b[i] = np.zeros(nodes_per_layer)
        self.b[layers] = np.zeros(3)

    # X = batch_states, y=batch_actions
    def do_minibatch(self, batch_states, batch_actions):
        # forward propogation
        acache = [0 for n in range(self.layers + 1)]
        rcache = [0 for n in range(self.layers)]
        A = batch_states

        for layer_num in range(self.layers):
            Z, acache[layer_num] = affine_forward(A, self.W[layer_num], self.b[layer_num])
            A, rcache[layer_num] = ReLU_forward(Z)
        F, acache[self.layers] = affine_forward(A, self.W[self.layers], self.b[self.layers])

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

    def get_output(self, inputs):
        inputs = self.normalize(inputs)
        A = inputs
        for layer_num in range(self.layers):
            Z, _ = affine_forward(A, self.W[layer_num], self.b[layer_num])
            A, _ = ReLU_forward(Z)
        F, _ = affine_forward(A, self.W[self.layers], self.b[self.layers])
        return F

    def get_action_num(self, state):
        return np.argmax(self.get_output(state))

    def get_action(self, state):
        return action_num_to_action(self.get_action_num(state))

    def do_epoch(self):
        order = np.arange(len(self.train_actions))
        np.random.shuffle(order)
        total_loss = 0

        for batch_num in range(len(self.train_actions) // batch_size):
            batch_states = np.array([self.train_states[order[i]] for i in range(batch_num * batch_size, min(len(self.train_actions), ((batch_num+1) * batch_size) - 1))])
            batch_actions = np.array([self.train_actions[order[i]] for i in range(batch_num * batch_size, min(len(self.train_actions), ((batch_num+1) * batch_size) - 1))])

            total_loss += self.do_minibatch(batch_states, batch_actions)
        return total_loss

if __name__ == "__main__":
    #np.random.seed(24)

    states, actions = utils.get_data()
    learner = Deep_Learner(states, actions, num_layers, num_nodes_per_layer)

    out = learner.get_output(states[0:10])
    print(out)

    correct = 0
    for i in range(len(actions)):
        if learner.get_action_num(states[i]) == actions[i]:
            correct += 1
    print(correct)
    print(len(actions))

    for i in range(learning_epochs):
        print(learner.do_epoch())

    correct = 0
    for i in range(len(actions)):
        if learner.get_action_num(states[i]) == actions[i]:
            correct += 1
    print(correct)
    print(len(actions))

    out = learner.get_output(states[0:10])
    print(out)
