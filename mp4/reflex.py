import game
import math
import random
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def get_action(state):
    ball_x, ball_y, vel_x, vel_y, pad_y = state

    while ball_x <= 1:
        ball_x += vel_x
        ball_y += vel_y

        if ball_y < 0:
            ball_y = -ball_y
            vel_y = -vel_y
        elif ball_y > 1:
            ball_y = 2 - ball_y
            vel_y = -vel_y

        if ball_x < 0:
            ball_x = -ball_x
            vel_x = -vel_x

    if ball_y > pad_y+game.paddle_height:
        return game.Action.DOWN
    elif ball_y < pad_y:
        return game.Action.UP
    else:
        return game.Action.NOTHING

if __name__ == "__main__":
    random.seed(100)

    num_games = 200
    hist_arr = np.zeros(num_games, dtype=int)
    for i in range(num_games):
        g = game.Game()
        while not g.lost_game():
            g.do_frame(get_action(g.get_state()))
        hist_arr[i] = g.get_num_bounces()

    plt.hist(hist_arr)
    plt.title("Reflex Distribution of bounces for " + str(num_games) + " test games")
    plt.xlabel("Number of bounces")
    plt.ylabel("Count")
    plt.savefig("image/reflex_hist.png")

    print("Average bounces: " + str(np.sum(hist_arr) / 200))
