import sys
import pygame
import game
import game_human
import random
# import q_learning
# import utils
import reflex
# import deep_learner

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
        self.basicFont = pygame.font.SysFont(None, 48)
        self.i = 0

    def refresh(self, g, delay):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        ballpos = [30+round(719 * g.ball_x), round(719 * g.ball_y)]
        ballspeed = [round(719 * g.velocity_x), round(719 * g.velocity_y)]
        paddlepos = round(719 * g.paddle_y)
        humanpos = round(719 * g.human_y)
        num_bounches = g.get_num_bounces()

        self.screen.fill(white)
        text = self.basicFont.render(str(num_bounches), True, blue)
        textRect = text.get_rect()
        textRect.centerx = self.screen.get_rect().centerx
        textRect.centery = self.screen.get_rect().centery
        self.screen.blit(text, textRect)
        pygame.draw.rect(self.screen, black, (0,humanpos,30,720*0.2))
        pygame.draw.rect(self.screen, black, (750,paddlepos,30,720*0.2))
        pygame.draw.circle(self.screen, red, (ballpos[0], ballpos[1]), 10)
        pygame.draw.line(self.screen, blue, (ballpos[0], ballpos[1]), (ballpos[0]+ballspeed[0], ballpos[1]+ballspeed[1]))

        pygame.display.flip()
        # pygame.image.save(self.screen, "animation/"+str(self.i)+".png")
        self.i += 1
        pygame.time.delay(delay)

if __name__ == "__main__":
    exploration_count = 20
    C = 20
    gamma = 0.95
    training_games = 30000

    # print("training...")
    # agent = q_learning.Q_Learner(gamma, q_learning.example_alpha, q_learning.f_1)
    # for i in range(training_games):
    #     if (i % 1000 == 0): print("i: "+str(i))
    #     agent.do_game()
    # print("finished training!")

    learning_epochs = 500
    weight_scale = 0.01
    learning_rate = .1
    batch_size = 100
    num_layers = 3
    num_nodes_per_layer = 256

    # states, actions = utils.get_data()
    # learner = deep_learner.Deep_Learner(states, actions, num_layers, num_nodes_per_layer)

    # for i in range(learning_epochs):
    #     print("i: "+str(i)+" loss: "+str(learner.do_epoch()))

    pg = PongGUIHuman()
    pg.init()

    while True:
        g = game_human.GameHuman()
        pg.refresh(g, 50)
        while not g.lost_game():
            # action = agent.get_action(g.get_discrete_state())
            # action = learner.get_action(g.get_state())
            action = reflex.get_action(g.get_state())

            keys = pygame.key.get_pressed()
            human = game.Action.NOTHING
            if keys[pygame.K_UP]:
                human = game.Action.UP
            elif keys[pygame.K_DOWN]:
                human = game.Action.DOWN

            g.do_frame(action, human)
            pg.refresh(g, 50)
        pygame.time.delay(3000)
