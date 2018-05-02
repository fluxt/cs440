from enum import Enum
import random
import numpy as np

class Action(Enum):
    DOWN = 0.04
    NOTHING = 0.0
    UP = -0.04

paddle_height = 0.2
discrete_end_game_state = (-1, -1, -1, -1, -1)

class GameHuman:
    def __init__(self):
        self.ball_x = 0.5
        self.ball_y = 0.5
        self.velocity_x = 0.03
        self.velocity_y = 0.01
        self.paddle_y = 0.5 - (paddle_height / 2)
        self.human_y = 0.5 - (paddle_height / 2)

        self.current_reward = 0
        self.bounces = 0

    def lost_game(self):
        return self.ball_x > 1

    def lost_game_human(self):
        return self.ball_x < 0

    # returns the reward for the action taken (-1, 0, or 1)
    def do_frame(self, act, human):
        if self.lost_game():
            self.current_reward = -1
            return

        self.paddle_y += act.value
        self.human_y += human.value

        if (self.paddle_y < 0):
            self.paddle_y = 0
        elif (self.paddle_y + paddle_height > 1):
            self.paddle_y = 1 - paddle_height

        if (self.human_y < 0):
            self.human_y = 0
        elif (self.human_y + paddle_height > 1):
            self.human_y = 1 - paddle_height

        self.ball_x += self.velocity_x
        self.ball_y += self.velocity_y

        if (self.ball_y < 0):
            self.ball_y = -self.ball_y
            self.velocity_y = - self.velocity_y
        elif (self.ball_y > 1):
            self.ball_y = 2 - self.ball_y
            self.velocity_y = - self.velocity_y

        if (self.ball_x < 0 and self.human_y < self.ball_y < self.human_y + paddle_height):
            self.ball_x = - self.ball_x
            self.velocity_x = - self.velocity_x

            if (abs(self.velocity_x) < 0.03):
                self.velocity_x = 0.03 if self.velocity_x > 0 else -0.03

            self.velocity_y = self.velocity_y + random.uniform(-.03, .03)
            self.bounces += 1
            return

        elif (self.ball_x > 1 and self.paddle_y < self.ball_y < self.paddle_y + paddle_height):
            self.ball_x = 2 - self.ball_x
            self.velocity_x = - self.velocity_x + random.uniform(-.015, .015)

            if (abs(self.velocity_x) < 0.03):
                self.velocity_x = 0.03 if self.velocity_x > 0 else -0.03

            self.velocity_y = self.velocity_y + random.uniform(-.03, .03)
            self.bounces += 1
            return
        self.current_reward = 0

    def get_state(self):
        return np.array([self.ball_x, self.ball_y, self.velocity_x, self.velocity_y, self.paddle_y])

    def get_human_state(self):
        return np.array([1.0-self.ball_x, self.ball_y, -self.velocity_x, self.velocity_y, self.human_y])

    def get_discrete_state(self):
        return discrete_end_game_state if self.lost_game() else (int(self.ball_x * 12), int(self.ball_y * 12), -1 if self.velocity_x < 0 else 1, -1 if self.velocity_y < -0.015 else (1 if self.velocity_y > 0.015 else 0), 11 if self.paddle_y == 1 - paddle_height else int(12 * self.paddle_y / (1 - paddle_height)))

    def get_num_bounces(self):
        return self.bounces

if __name__ == "__main__":
    g = GameHuman()
    while not g.lost_game():
        g.do_frame(Action.NOTHING, Action.NOTHING)
