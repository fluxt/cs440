import game
import math

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
