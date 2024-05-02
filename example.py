import torch
import random
import numpy as np
from game import SnakeGameAI, Direction, Point
from model import Linear_QNet

class Agent:
    def __init__(self, model):
        self.model = model

    def get_action(self, state):
        state_tensor = torch.tensor(state, dtype=torch.float)
        with torch.no_grad():
            prediction = self.model(state_tensor)
        move = torch.argmax(prediction).item()
        final_move = [0, 0, 0]
        final_move[move] = 1
        return final_move

def play_game_with_model(model_path):
    model = Linear_QNet(11, 256, 3)
    model.load_state_dict(torch.load(model_path))
    model.eval()

    agent = Agent(model)
    game = SnakeGameAI()

    while True:
        state_old = game.get_state()  # Using get_state from SnakeGameAI
        final_move = agent.get_action(state_old)
        _, done, score = game.play_step(final_move)

        if done:
            print('Game over! Score:', score)
            break

if __name__ == '__main__':
    model_path = 'rl_model.pth'
    play_game_with_model(model_path)
