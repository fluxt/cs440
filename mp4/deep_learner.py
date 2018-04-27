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


def ReLU(x):
    return max(x, 0)

if __name__ == "__main__":
    np.random.seed(24)

    states, actions = utils.get_data()
    learner = Deep_Learner(states, actions, ReLU)

    for i in range(1):
        learner.do_epoch()
