import time

import torch
import random
import numpy as np
from collections import deque
from snakeGame import SnakeGameAI, Direction, Point
from model import Linear_QNet, QTrainer
import pygame

font = pygame.font.Font('arial.ttf', 25)


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        # self.epsilon = 0 # randomness

        self.epsilon = 0  # randomness

        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)

        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)),

            # Danger left
            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)),

            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Food location
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y  # food down
            ]

        return np.array(state, dtype=int)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        # if random.randint(0, 200) < self.epsilon:
        #     move = random.randint(0, 2)
        #     final_move[move] = 1
        # else:
        state0 = torch.tensor(state, dtype=torch.float)
        prediction = self.model(state0)
        move = torch.argmax(prediction).item()
        final_move[move] = 1

        return final_move


import button
import agent1

import agent2
import snakeGame2

pygame.init()

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")


font = pygame.font.SysFont("arialblack", 30)
text_col = (255,255,255)



# button images
img = pygame.image.load("assets/easyButton.png").convert_alpha()
img1 = pygame.image.load("assets/mediumButton.png").convert_alpha()
img2 = pygame.image.load("assets/hardButton.png").convert_alpha()
img3 = pygame.image.load("assets/qmarkButton.png").convert_alpha()
img4 = pygame.image.load("assets/guideImage.png").convert_alpha()
img5 = pygame.image.load("assets/backImage.png").convert_alpha()

img_button = button.Button(235,70, img, 0.4)
img_button1 = button.Button(180,185, img1, 0.4)
img_button2 = button.Button(235,300, img2, 0.4)
img_button3 = button.Button(550,370, img3, 0.3)
img_button4 = button.Button(20,20, img4, 1.07)
img_button5 = button.Button(560,10, img5, 0.3)

bg = pygame.image.load("assets/StartScreen.png").convert()

def draw_text(text,font,text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))


# game variables
start_key = False
menu_state = "main"
try_state = "123"
try_state1 = "123"
try_state2 = "123"

if __name__ == '__main__':
    agent = Agent()
    agent.model.load()

    agent1 = agent1.Agent()
    agent1.model.load()

    game = SnakeGameAI()

    game1 = SnakeGameAI()

    agent2 = agent2.Agent()
    agent2.model.load()
    game2 = snakeGame2.SnakeGameAI()


    run = True
    running = True
    running1 = True

    while run:

        screen.fill((52, 78, 91))
        # screen.fill((88,84,84))
        if start_key == True:

            if menu_state == "main":
                # print(try_state)

                if img_button.draw(screen):
                    menu_state = "start"
                if img_button1.draw(screen):
                    menu_state = "medium"
                if img_button2.draw(screen):
                    menu_state = "hard"
                if img_button3.draw(screen):
                    menu_state = "guide"
            elif menu_state == "start":
                running2 = True
                while running2:

                    if try_state2 == "menubackyu":
                        menu_state = "main"
                        # try_state = " "
                        game2.pause = False
                        try_state2 = ""
                        # print("here")
                        game2.reset()
                        break

                    if game2.pause:
                        game2.unpause()
                        try_state2 = game2.back

                    try:
                        if not game2.pause:
                            # get old state
                            state_old = agent2.get_state(game2)
                            # get move
                            final_move = agent2.get_action(state_old)
                            # perform move and get new state
                            game2.play_step(final_move)
                            state_new = agent2.get_state(game2)
                    except Exception as e:

                        game2.pause = True
                        game2.draw_death_text()
                        try_state2 = game2.back
                        print(e)
            elif menu_state == "medium":
                # print("med")
                running1 = True
                while running1:

                    if try_state1 == "menubackyu":
                        menu_state = "main"
                        # try_state = " "
                        game1.pause = False
                        try_state1 = ""
                        # print("here")
                        game1.reset()
                        break

                    if game1.pause:
                        game1.unpause()
                        try_state1 = game1.back

                    try:
                        if not game1.pause:
                            # get old state
                            state_old = agent1.get_state(game1)
                            # get move
                            final_move = agent1.get_action(state_old)
                            # perform move and get new state
                            game1.play_step(final_move)
                            state_new = agent1.get_state(game1)
                    except Exception as e:

                        game1.pause = True
                        game1.draw_death_text()
                        try_state1 = game.back
                        print(e)
            elif menu_state == "hard":
                # if (running == False and try_state != "menuback"):
                #     running = True

                running = True
                while running:

                    if try_state == "menubackyu":
                        menu_state = "main"
                        # try_state = " "
                        game.pause = False
                        try_state = ""
                        # print("here")
                        game.reset()
                        break


                    if game.pause:
                        game.unpause()
                        try_state = game.back

                    try:
                        if not game.pause:
                            # get old state
                            state_old = agent.get_state(game)
                            # get move
                            final_move = agent.get_action(state_old)
                            # perform move and get new state
                            game.play_step(final_move)
                            state_new = agent.get_state(game)
                    except Exception as e:

                        game.pause = True
                        game.draw_death_text()
                        try_state = game.back
                        print(e)
            elif menu_state == "guide":
                if img_button4.draw(screen):
                    pass
                if img_button5.draw(screen):
                    menu_state = "main"


        else:
            # draw_text("Press Space to pause", font, text_col, 150, 350)
            screen.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_key = True
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()

    pygame.quit()




