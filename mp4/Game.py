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

    def do_frame(self, act):
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
