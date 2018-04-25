import sys, pygame
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

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # ballpos = [720 * ball_x, 720 * ball_y]
    # paddlepos = [720 * paddle_y]

    ballpos = [x+y for x,y in zip(ballpos, ballspeed)]
    paddlepos = paddlepos + paddlespeed
    if ballpos[0] <= 0 or ballpos[0] >= width-30:
        ballspeed[0] = -ballspeed[0]
    if ballpos[1] <= 0 or ballpos[1] >= height:
        ballspeed[1] = -ballspeed[1]
    if paddlepos <= 0 or paddlepos >= height*0.8:
        paddlespeed = - paddlespeed

    screen.fill(white)
    pygame.draw.circle(screen, red, (ballpos[0], ballpos[1]), 10)
    pygame.draw.rect(screen, black, (720,paddlepos,30,144))
    pygame.display.flip()
