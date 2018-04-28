import game

def get_action(state):
    ball_x, ball_y, vel_x, vel_y, pad_y = state
    x_dist = 1 + ball_x vel_x < 0 else 1 - ball_x
    y_dist = vel_y / abs(vel_x)
    y_goal = (y_dist + ball_y)
    y_goal = y_goal % 1 if y_goal % 2 < 1 else -(y_goal % 1)
    if (y_goal > pad_y + game.paddle_height):
        return game.Action.DOWN
    elif (y_goal < pad_y):
        return game.Action.UP
    else:
        return game.Action.NOTHING
