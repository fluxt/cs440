import utils
import game
import numpy as np

learning_epochs = 5

weight_scale = 0.02
learning_rate = .5
batch_size = 300
num_layers = 2
num_nodes_per_layer = 100

# also returns (A, W, b) for caching
def affine_forward(A, W, b):
    return ((A.dot(W)) + b), (A, W, b)

# (A, W, b) passed in as 'cache'
# returns dA, dW, db
def affine_backward(dZ, cache):
    A, W, b = cache
    dA = np.zeros(A.shape)
    for i, k in np.ndindex(dA.shape):
        dA[i][k] = np.sum(dZ[i] * W[k])

    dW = np.zeros(W.shape)
    for k, j in np.ndindex(dW.shape):
        dW[k][j] = np.sum(A[:,k] * dZ[:,j])

    db = np.zeros(b.shape)
    for j in range(db.shape[0]):
        db[j] = np.sum(dZ[:,j])
    return dA, dW, db


# also returns Z for caching
def ReLU_forward(Z):
    ret = Z.copy()
    ret[ret < 0] = 0
    return ret, Z

# Z passed in as 'cache'
def ReLU_backward(dA, cache):
    Z = cache
    dZ = dA.copy()
    dZ[Z < 0] = 0
    return dZ

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
    # layers is the number of inner layers
    def __init__(self, training_states, training_actions, layers, nodes_per_layer):
        self.train_states = training_states
        self.train_outputs = np.zeros((len(training_actions), 3))
        self.train_actions = training_actions

        self.layers = layers
        self.W = np.random.uniform(0, weight_scale, size=(layers-1, nodes_per_layer, nodes_per_layer))
        self.W_in = np.random.uniform(0, weight_scale, size=(5, nodes_per_layer))
        self.W_out = np.random.uniform(0, weight_scale, size=(nodes_per_layer, 3))
        self.b = np.zeros((layers, nodes_per_layer))
        self.b_out = np.zeros(3)

    def get_output(self, inputs):
        Z, _ = affine_forward(inputs, self.W_in, self.b[0])
        Z, _ = ReLU_forward(Z)
        for n in range(self.layers - 1):
            Z, _ = affine_forward(Z, self.W[n], self.b[n+1])
            Z, _ = ReLU_forward(Z)
        return affine_forward(Z, self.W_out, self.b_out)[0]

    def get_action_num(self, state):
        return np.argmax(self.get_output(state))

    def get_action(self, state):
        return action_num_to_action(self.get_action_num(state))

    # X = batch_states, y=batch_actions
    def do_minibatch(self, batch_states, batch_actions):
        # forward propogation
        acache = [0 for n in range(self.layers + 1)]
        rcache = [0 for n in range(self.layers)]
        Z, acache[0] = affine_forward(batch_states, self.W_in, self.b[0])
        A, rcache[0] = ReLU_forward(Z)

        for layer_num in range(1, self.layers):
            Z, acache[layer_num] = affine_forward(A, self.W[layer_num-1], self.b[layer_num])
            A, rcache[layer_num] = ReLU_forward(Z)
        F, acache[self.layers] = affine_forward(A, self.W_out, self.b_out)

        loss, dF = cross_entropy(F, batch_actions)

        # back-propogation
        dW = [0 for n in range(self.layers + 1)]
        db = [0 for n in range(self.layers + 1)]

        dA, dW[self.layers], db[self.layers] = affine_backward(dF, acache[self.layers])
        for layer_num in range(self.layers - 1, -1, -1):
            dZ = ReLU_backward(dA, rcache[layer_num])
            dA, dW[layer_num], db[layer_num] = affine_backward(dZ, acache[layer_num])

        # gradient descent
        self.W_in -= learning_rate * dW[0]
        self.W_out -= learning_rate * dW[self.layers]
        self.b[0] -= learning_rate * db[0]
        self.b_out -= learning_rate * db[self.layers]

        for i in range(1, self.layers):
            self.W[i-1] -= learning_rate * dW[i]
            self.b[i] -= learning_rate * db[i]
        return loss

    def do_epoch(self):
        order = np.arange(len(self.train_states))
        np.random.shuffle(order)

        total_loss = 0

        for batch_num in range(len(self.train_states) // batch_size):
            batch_states = []
            batch_actions = []
            for i in range(batch_num * batch_size, min(len(self.train_states), ((batch_num+1) * batch_size) - 1)):
                batch_states.append(self.train_states[order[i]])
                batch_actions.append(self.train_actions[order[i]])
            batch_states = np.array(batch_states)
            batch_actions = np.array(batch_actions)

            total_loss += self.do_minibatch(batch_states, batch_actions)
        return total_loss

if __name__ == "__main__":
    np.random.seed(24)

    states, actions = utils.get_data()
    learner = Deep_Learner(states, actions, num_layers, num_nodes_per_layer)

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
