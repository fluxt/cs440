import sys
import pygame
import game
import random
import q_learning

size = width, height = [750, 720]
black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]

class PongGUI():
    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(size)

    def refresh(self, g, delay):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        ballpos = [round(719 * g.ball_x), round(719 * g.ball_y)]
        ballspeed = [round(719 * g.velocity_x), round(719 * g.velocity_y)]
        paddlepos = round(719 * g.paddle_y)

        self.screen.fill(white)
        pygame.draw.rect(self.screen, black, (720,paddlepos,30,144))
        pygame.draw.circle(self.screen, red, (ballpos[0], ballpos[1]), 10)
        pygame.draw.line(self.screen, blue, (ballpos[0], ballpos[1]), (ballpos[0]+ballspeed[0], ballpos[1]+ballspeed[1]))

        pygame.display.flip()
        pygame.time.delay(delay)

if __name__ == "__main__":
    exploration_count = 20
    C = 20
    gamma = 0.95
    training_games = 30000

    print("training...")
    agent = q_learning.Q_Learner(gamma, q_learning.example_alpha, q_learning.f_1)
    for i in range(training_games):
        if (i % 1000 == 0): print("i: "+str(i))
        agent.do_game()
    print("finished training!")

    pg = PongGUI()
    pg.init()

    while True:
        g = game.Game()
        pg.refresh(g, 50)
        while not g.lost_game():
            action = agent.get_action(g.get_discrete_state())
            g.do_frame(action)
            pg.refresh(g, 50)
