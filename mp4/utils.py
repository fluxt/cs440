import game
import numpy as np

data_file = "data/expert_policy.txt"

# get the data for the deep-learning agent
def get_data():
    lines = open(data_file).readlines()

    states = np.zeros((len(lines), 5), dtype=float)
    actions = np.zeros(len(lines), dtype=int)

    for i in range(len(lines)):
        strs = lines[i].split(' ')
        states[i] = np.array([float(n) for n in strs[:-1]])
        actions[i] = int(float(strs[5]))

    return states, actions
