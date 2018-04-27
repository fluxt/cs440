import sys, pygame
import game
import random

pygame.init()

size = width, height = [750, 720]
black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]

screen = pygame.display.set_mode(size)

ballpos = [0,0]
ballspeed = [1, 1]
paddlepos = 0

def refresh(g, delay):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    ballpos = [round(719 * g.ball_x), round(719 * g.ball_y)]
    ballspeed = [round(719 * g.velocity_x), round(719 * g.velocity_y)]
    paddlepos = round(719 * g.paddle_y)

    screen.fill(white)
    pygame.draw.rect(screen, black, (720,paddlepos,30,144))
    pygame.draw.circle(screen, red, (ballpos[0], ballpos[1]), 10)
    pygame.draw.line(screen, blue, (ballpos[0], ballpos[1]), (ballpos[0]+ballspeed[0], ballpos[1]+ballspeed[1]))

    pygame.display.flip()
    pygame.time.delay(delay)

if __name__ == "__main__":
    while True:
        g = game.Game()
        refresh(g, 100)
        while not g.lost_game():
            action = random.choice([game.Action.NOTHING,game.Action.UP,game.Action.DOWN])
            g.do_frame(action)
            refresh(g, 100)
