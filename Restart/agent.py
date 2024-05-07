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

def train():
    agent = Agent()
    agent.model.load()
    game = SnakeGameAI()
    running = True
    while running:
        if game.player_dead:
            # Draw death text and keep the game window open
            game.draw_death_text()
            break  # Exit the loop when the player is dead
        else:
            # get old state
            state_old = agent.get_state(game)
            # get move
            final_move = agent.get_action(state_old)
            # perform move and get new state
            game.play_step(final_move)
            state_new = agent.get_state(game)


    game.draw_death_text()








if __name__ == '__main__':
    agent = Agent()
    agent.model.load()
    game = SnakeGameAI()
    running = True


    while running:
        if game.pause:
            game.unpause()
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

            print(e)



        # if game.player_dead:
        #     # Draw death text and keep the game window open
        #     # game.update_ui()
        #     pause = True
        #     game.display.fill((0,0,0))
        #     game.draw_death_text()
        #     # print("asd")
        #     # time.sleep(50)
        #     # break  # Exit the loop when the player is dead
        # else:
        #     if (pause == False):
        #         # get old state
        #         state_old = agent.get_state(game)
        #         # get move
        #         final_move = agent.get_action(state_old)
        #         # perform move and get new state
        #         game.play_step(final_move)
        #         state_new = agent.get_state(game)



