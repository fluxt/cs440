from enum import Enum

class Action(Enum):
    UP = -0.04
    NOTHING = 0.0
    DOWN = 0.04

paddle_height = 0.2

class Game:
    def __init__(self):
        self.ball_x = 0.5
        self.ball_y = 0.5
        self.velocity_x = 0.03
        self.velocity_y = 0.01
        self.paddle_y = 0.5 - (paddle_height / 2)

    def lost_game(self):
        return (self.ball_x > 1)

    # returns the reward for the action taken (-1, 0, or 1)
    def do_frame(self, act):
        if self.lost_game():
            return -1

        self.paddle_y += act.value

        if (self.paddle_y < 0):
            self.paddle_y = 0
        elif (self.paddle_y + paddle_height > 1):
            self.paddle_y = 1 - paddle_height

        self.ball_x += self.velocity_x
        self.ball_y += self.velocity_y

        if (self.ball_y < 0):
            self.ball_y = -self.ball_y
            self.velocity_y = - self.velocity_y
        elif (self.ball_y > 1):
            self.ball_y = 2 - self.ball_y
            self.velocity_y = - self.velocity_y

        if (self.ball_x < 0):
            self.ball_x = - self.ball_x
            self.ball_y = - self.velocity_x
        elif (self.ball_x > 1 and self.paddle_y < self.ball_y < self.paddle_y - paddle_height):
            self.ball_x = 2 - self.ball_x
            self.velocity_x = - velocity_x + random(-.015, .015)

            if (abs(self.velocity_x) < 0.03):
                self.velocity_x = 0.03 if self.velocity_x > 0 else -0.03

            self.velocity_y = velocity_y + random(-.03, .03)
            return 1
        return 0

    def get_state(self):
        return (self.ball_x, self.ball_y, self.velocity_x, self.velocity_y, self.paddle_y)

    def get_discrete_state(self):
        return (-1, -1, -1, -1, -1) if lost_game else (int(self.ball_x * 12), int(self.ball_y * 12), -1 if self.velocity_x < 0 else 1, -1 if self.velocity_y < -0.015 elif self.velocity_y > 0.015 1 else 0, 11 if paddle_y == 1 - paddle_height else int(12 * paddle_y(1 - paddle_height)))
