import utils
import game
import numpy as np

class Deep_Learner:
    def __init__(self, training_states, training_actions, activation_function):
        self.train_states = training_states
        self.train_actions = training_actions
        self.activation_function = activation_function

    def do_epoch():
        

def ReLU(x):
    return max(0, x)

if __name__ == "__main__":
    states, actions = utils.get_data()
    learner = Deep_Learner(states, actions, ReLU)
