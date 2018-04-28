import game
import math

def get_action(state):
    ball_x, ball_y, vel_x, vel_y, pad_y = state
    x_dist = 1 + ball_x if vel_x < 0 else 1 - ball_x
    y_dist = x_dist * vel_y / abs(vel_x)
    y_goal = (y_dist + ball_y)

    

    pad_center = pad_y + (game.paddle_height / 2)
    if (y_goal > pad_center):
        return game.Action.DOWN
    elif (y_goal < pad_center):
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
    num_games = 1000
    sum = 0
    for i in range(num_games):
        g = game.Game()
        while not g.lost_game():
            g.do_frame(get_action(g.get_state()))
        sum += g.get_num_bounces()
    print(sum / num_games)
