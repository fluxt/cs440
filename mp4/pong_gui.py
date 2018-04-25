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
paddlespeed = 1

g = game.Game()

# while True:
while not g.lost_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    ballpos = [round(720 * g.ball_x), round(720 * g.ball_y)]
    ballspeed = [round(720 * g.velocity_x), round(720 * g.velocity_y)]
    paddlepos = round(720 * g.paddle_y)




    ballpos = [x+y for x,y in zip(ballpos, ballspeed)]
    paddlepos = paddlepos + paddlespeed
    if ballpos[0] <= 0 or ballpos[0] >= width-30:
        ballspeed[0] = -ballspeed[0]
    if ballpos[1] <= 0 or ballpos[1] >= height:
        ballspeed[1] = -ballspeed[1]
    if paddlepos <= 0 or paddlepos >= height*0.8:
        paddlespeed = - paddlespeed

    screen.fill(white)
    pygame.draw.rect(screen, black, (720,paddlepos,30,144))
    pygame.draw.circle(screen, red, (ballpos[0], ballpos[1]), 10)
    pygame.draw.line(screen, blue, (ballpos[0], ballpos[1]), (ballpos[0]+ballspeed[0], ballpos[1]+ballspeed[1]))

    pygame.display.flip()

    g.do_frame(random.choice([game.Action.UP, game.Action.NOTHING, game.Action.DOWN]))

    pygame.time.delay(50)
