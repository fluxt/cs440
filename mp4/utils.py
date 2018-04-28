import game
import numpy as np

data_file = "data/expert_policy.txt"

def get_data():
    lines = open(data_file).readlines()

    states = np.zeros((len(lines), 5), dtype=float)
    actions = []

    for i in range(len(lines)):
        strs = lines[i].split(' ')
        states[i] = np.array([float(n) for n in strs[:-1]])
        act_num = int(float(strs[5]))
        actions.append(act_num)

    return states, actions
