import game
import math

def get_action(state):
    ball_x, ball_y, vel_x, vel_y, pad_y = state
    x_dist = 1 + ball_x if vel_x < 0 else 1 - ball_x
    y_dist = x_dist * vel_y / abs(vel_x)
    y_goal = (y_dist + ball_y)
    
    if (y_goal > pad_y + game.paddle_height):
        return game.Action.DOWN
    elif (y_goal < pad_y):
        return game.Action.UP
    else:
        return game.Action.NOTHING

def get_action2(state):
    ball_x, ball_y, vel_x, vel_y, pad_y = state
    if vel_x < 0:
        ticks_rebound = math.ceil(1 + ball_x/abs(vel_x))
    else:
        ticks_rebound = math.ceil(1 - ball_x/abs(vel_x))
    
if __name__ == "__main__":
    for i in range(20):
        g = game.Game()
        while not g.lost_game():
            g.do_frame(get_action(g.get_state()))
        print(g.get_num_bounces())
