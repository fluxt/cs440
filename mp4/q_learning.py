import game
from collections import defaultdict
import random
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# number of times the agent should try an action at a state
exploration_count = 20
# constant for our alpha learning-rate function
C = 20
# the discount factor for our agent
gamma = 0.95

num_training_games = 30000
num_test_games = 200

class Q_Learner:
    def __init__(self, gamma, learning_rate_func, exploration_func):
        # the dictionary for the quality of an action at a specific state - indexed with a tuple (state, action)
        self.q_dict = defaultdict(float)

        # the dictionary for the number of times the agent has taken an action at a state - indexed same as q_dict
        self.n_dict = defaultdict(int)

        self.discount_factor = gamma

        self.learning_rate_func = learning_rate_func

        self.exploration_func = exploration_func

    def get_action(self, state):
        max_f = -2
        best = 0
        for act in game.Action:
            f_val = self.exploration_func(self.q_dict[(state, act)], self.n_dict[(state, act)])
            if f_val > max_f:
                max_f = f_val
                best = act
        return best

    def do_game(self):
        g = game.Game()

        prev_state = 0
        first_state = True
        prev_action = 0
        prev_reward = 0

        while (True):
            current_state = g.get_discrete_state()
            current_reward = g.get_current_reward()

            if prev_state == game.discrete_end_game_state:
                for act in game.Action:
                    self.q_dict[(prev_state, act)] = -1
                return g.get_num_bounces()

            if not first_state:
                self.n_dict[(prev_state, prev_action)] += 1
                max_q = max([self.q_dict[(current_state, act)] for act in game.Action])

                prev_idx = (prev_state, prev_action)
                self.q_dict[prev_idx] += self.learning_rate_func(self.n_dict[prev_idx]) * (prev_reward + (self.discount_factor * max_q) - self.q_dict[prev_idx])

            prev_state = current_state
            prev_action = self.get_action(current_state)
            prev_reward = current_reward
            first_state = False

            g.do_frame(prev_action)


def f(u, n):
    if n < exploration_count:
        return float('inf')
    else:
        return u

def alpha(n):
    return C / (C + n)

if __name__ == "__main__":
    random.seed(18)
    q = Q_Learner(gamma, alpha, f)

    plot_smoothing_size = 300
    bounces_arr = np.zeros(num_training_games // plot_smoothing_size)
    sum = 0
    for i in range(num_training_games):
        if (i % 1000 == 0):
            print("i=" + str(i))
        if (i > 0 and i % plot_smoothing_size == 0):
            bounces_arr[i // plot_smoothing_size] = sum / plot_smoothing_size
            sum = 0
        sum += q.do_game()

    plt.plot(np.arange(0, num_training_games, plot_smoothing_size), bounces_arr)
    plt.title("TD Q-Learning Bounces per Training Game")
    plt.ylabel("Number of Bounces")
    plt.xlabel("Game Number")
    plt.xlim((0, num_training_games))
    plt.savefig("image/q_plot.png")
    plt.clf()

    bounces_hist_arr = np.zeros(num_test_games, dtype=int)
    sum = 0
    for i in range(num_test_games):
        val = q.do_game()
        bounces_hist_arr[i] = val
        sum += val

    plt.hist(bounces_hist_arr, bins = max(bounces_hist_arr) - 1)
    plt.title("TD Q-Learning Distribution of bounces for " + str(num_test_games) + " test games")
    plt.xlabel("Number of bounces")
    plt.ylabel("Count")
    plt.savefig("image/q_hist.png")

    print("Test average: " + str(sum / 200))
