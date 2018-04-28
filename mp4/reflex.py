import game
import math

def get_action(state):
    x_pos, y_pos, vel_x, vel_y, pad_y = state
    x_dist = 1 + x_pos if vel_x < 0 else 1 - x_pos
    y_dist = x_dist * vel_y / abs(vel_x)
    y_goal = (y_dist + y_pos)

    while y_goal < 0 or y_goal > 1:
        if (y_goal < 0):
            y_goal *= -1
        else:
            y_goal = 2 - y_goal

    pad_center = pad_y + (game.paddle_height / 2)
    if (y_goal > pad_center):
        return game.Action.DOWN
    elif (y_goal < pad_center):
        return game.Action.UP
    else:
        return game.Action.NOTHING

def get_action2(state):
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

    if (ball_y > pad_y+game.paddle_height):
        return game.Action.DOWN
    elif (ball_y < pad_y):
        return game.Action.UP
    else:
        return game.Action.NOTHING

if __name__ == "__main__":
    num_games = 200
    sum = 0
    for i in range(num_games):
        g = game.Game()
        while not g.lost_game():
            g.do_frame(get_action2(g.get_state()))
        sum += g.get_num_bounces()
    print(sum / num_games)
