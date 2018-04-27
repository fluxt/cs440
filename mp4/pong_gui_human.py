import sys
import pygame
import game
import game_human
import random
import q_learning

size = width, height = [780, 720]
black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]

class PongGUIHuman():
    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        # self.i = 0

    def refresh(self, g, delay):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        ballpos = [30+round(719 * g.ball_x), round(719 * g.ball_y)]
        ballspeed = [round(719 * g.velocity_x), round(719 * g.velocity_y)]
        paddlepos = round(719 * g.paddle_y)
        humanpos = round(719 * g.human_y)

        self.screen.fill(white)
        pygame.draw.rect(self.screen, black, (0,humanpos,30,720*0.2))
        pygame.draw.rect(self.screen, black, (750,paddlepos,30,720*0.2))
        pygame.draw.circle(self.screen, red, (ballpos[0], ballpos[1]), 10)
        pygame.draw.line(self.screen, blue, (ballpos[0], ballpos[1]), (ballpos[0]+ballspeed[0], ballpos[1]+ballspeed[1]))

        pygame.display.flip()
        # pygame.image.save(self.screen, "animations/"+str(self.i)+".png")
        # self.i += 1
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

    pg = PongGUIHuman()
    pg.init()

    while True:
        g = game_human.GameHuman()
        pg.refresh(g, 50)
        while not g.lost_game():
            action = agent.get_action(g.get_discrete_state())

            keys = pygame.key.get_pressed()
            human = game.Action.NOTHING
            if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
                human = game.Action.UP
            elif not keys[pygame.K_UP] and keys[pygame.K_DOWN]:
                human = game.Action.DOWN

            g.do_frame(action, human)
            pg.refresh(g, 50)
