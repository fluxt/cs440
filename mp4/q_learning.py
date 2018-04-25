import game
from collections import defaultdict
#import pong_gui as gui

exploration_count = 10
C = 5
gamma = 0.95

class Q_Learner:
    def __init__(self, gamma, learning_rate_func, exploration_func):
        # the dictionary for the quality of an action at a specific state - indexed with a tuple (state, action)
        self.q_dict = defaultdict(float)

        # the dictionary for the number of times the agent has taken an action at a state - indexed same as q_dict
        self.n_dict = defaultdict(int)

        self.discount_factor = gamma

        self.learning_rate_func = learning_rate_func

        self.exploration_func = exploration_func

    def do_game(self, display):
        g = game.Game()

        prev_state = 0
        first_state = True
        prev_action = 0
        prev_reward = 0

        while (True):
            #if display:
                #gui.refresh(g, 10)
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

            # set prev_action to the action you want to take
            max_f = -2
            for act in game.Action:
                f_val = self.exploration_func(self.q_dict[(current_state, act)], self.n_dict[(current_state, act)])
                if f_val > max_f:
                    max_f = f_val
                    prev_action = act
            prev_reward = current_reward
            first_state = False

            g.do_frame(prev_action)

def f_1(u, n):
    if n < exploration_count:
        return float('inf')
    else:
        return u

#def f_2(u, n, eps):


def example_alpha(n):
    return C / (C + n)

if __name__ == "__main__":
    q = Q_Learner(gamma, example_alpha, f_1)

    sum = 0
    for i in range(100000):
        if (i % 1000 == 0):
            print("" + str(i) + " : " + str((sum / 1000)))
            sum = 0
        sum += q.do_game(False)

    sum = 0
    for i in range(200):
        sum += q.do_game(False)

    print(sum / 200)
