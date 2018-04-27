import utils
import game
import numpy as np

learning_epochs = 1

weight_scale = 0.1
learning_rate = 0.1
batch_size = 100
num_layers = 4
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
        dW[k][j] = np.sum(A[:][k] * dZ[:][j])

    db = np.zeros(b.shape)
    for j in range(db.shape[0]):
        db[j] = np.sum(dZ[:][j])


# also returns Z for caching
def ReLU_forward(Z):
    ret = Z.copy()
    ret[ret < 0] = 0
    return ret, Z

# Z passed in as 'cache'
def ReLU_backward(dA, cache):
    Z = cache
    dZ = dA.copy()
    dZ[Z==0] = 0
    return dZ

def cross_entropy(F, y):
    n = y.shape[0]
    for i in range()

def action_to_vector(act):
    if act == game.Action.UP:
        return np.array([1, 0, 0])
    elif act == game.Action.NOTHING:
        return np.array([0, 1, 0])
    else:
        return np.array([0, 0, 1])

def vector_to_action(vec):
    if vec[0] > vec[1] and vec[0] > vec[2]:
        return game.Action.UP
    elif vec[1] > vec[0] and vec[1] > vec[2]:
        return game.Action.NOTHING
    else:
        return game.Action.DOWN

class Deep_Learner:
    # layers is the number of inner layers
    def __init__(self, training_states, training_actions, layers, nodes_per_layer):
        self.train_states = training_states
        self.train_outputs = np.zeros((len(training_actions), 3))
        for i in range(len(training_actions)):
            self.train_outputs[i] = action_to_vector(training_actions[i])

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

    def get_action(self, state):
        return vector_to_action(self.get_output(state))

    def do_minibatch(self, batch_states, batch_actions):
        acaches = [0 for n in range(self.layers + 2)]
        rcaches = [0 for n in range(self.layers + 1)]



    def do_epoch(self):
        order = np.arange(len(self.train_states))
        np.random.shuffle(order)

        for batch_num in range(len(self.train_states) // batch_size):
            batch_states = []
            batch_outputs = []
            for i in range(batch_num * batch_size, min(len(self.train_states), ((batch_num+1) * batch_size) - 1)):
                batch_states.append(self.train_states[order[i]])
                batch_outputs.append(self.train_outputs[order[i]])
            batch_states = np.array(batch_states)
            batch_outputs = np.array(batch_outputs)

            self.do_minibatch(batch_states, batch_outputs)

if __name__ == "__main__":
    np.random.seed(24)

    states, actions = utils.get_data()
    learner = Deep_Learner(states, actions, 4, 256)

    out = learner.get_output(states[0:10])
    print(out)

    for i in range(learning_epochs):
        learner.do_epoch()
