from enum import Enum
import random
import numpy as np

# actions an agent can take
class Action(Enum):
    DOWN = 0.04
    NOTHING = 0.0
    UP = -0.04

paddle_height = 0.2
# unique state for the end-game (when the agent has lost) for the q_learning and sarsa agents
discrete_end_game_state = (-1, -1, -1, -1, -1)

class Game:
    def __init__(self):
        self.ball_x = 0.5
        self.ball_y = 0.5
        self.velocity_x = 0.03
        self.velocity_y = 0.01
        self.paddle_y = 0.5 - (paddle_height / 2)

        # the reward to the agent for the current state
        self.current_reward = 0

        # the number of bounces for this game
        self.bounces = 0

    def lost_game(self):
        return (self.ball_x > 1)

    # does one time tick (frame) in the game
    def do_frame(self, act):
        if self.lost_game():
            self.current_reward = -1
            return

        # do the agent's action
        self.paddle_y += act.value

        # clip the paddle to be entirely within the bounds
        if (self.paddle_y < 0):
            self.paddle_y = 0
        elif (self.paddle_y + paddle_height > 1):
            self.paddle_y = 1 - paddle_height

        # update the ball's position
        self.ball_x += self.velocity_x
        self.ball_y += self.velocity_y

        # do bounces off the top/bottom of the screen
        if (self.ball_y < 0):
            self.ball_y = -self.ball_y
            self.velocity_y = - self.velocity_y
        elif (self.ball_y > 1):
            self.ball_y = 2 - self.ball_y
            self.velocity_y = - self.velocity_y

        # do bounces with the left wall
        if (self.ball_x < 0):
            self.ball_x = - self.ball_x
            self.velocity_x = - self.velocity_x
        elif (self.ball_x > 1 and self.paddle_y < self.ball_y < self.paddle_y + paddle_height):
            # do bounces against the paddle
            self.ball_x = 2 - self.ball_x
            self.velocity_x = - self.velocity_x + random.uniform(-.015, .015)

            if (abs(self.velocity_x) < 0.03):
                self.velocity_x = 0.03 if self.velocity_x > 0 else -0.03

            self.velocity_y = self.velocity_y + random.uniform(-.03, .03)
            self.current_reward = 1
            self.bounces += 1
            return
        self.current_reward = 0

    # get the continuous state for the game
    def get_state(self):
        return np.array([self.ball_x, self.ball_y, self.velocity_x, self.velocity_y, self.paddle_y])

    # get the discrete state for the game
    def get_discrete_state(self):
        return discrete_end_game_state if self.lost_game() else (int(self.ball_x * 12), int(self.ball_y * 12), -1 if self.velocity_x < 0 else 1, -1 if self.velocity_y < -0.015 else (1 if self.velocity_y > 0.015 else 0), 11 if self.paddle_y == 1 - paddle_height else int(12 * self.paddle_y / (1 - paddle_height)))

    # get the reward for the agent at the current state (1 if it just bounced, -1 if it has lost, 0 otherwise)
    def get_current_reward(self):
        return self.current_reward

    # get the number of paddle-bounces so far in the game
    def get_num_bounces(self):
        return self.bounces
