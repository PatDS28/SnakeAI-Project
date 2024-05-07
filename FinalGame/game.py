import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

GREEN1 = (0, 255, 0)
GREEN2 = (100, 255, 0)
PINK = (255, 192, 203)

BLOCK_SIZE = 20
SPEED = 10
PLAYER_SPEED = 8

class SnakeGameAI:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display


        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.clock_player = pygame.time.Clock()

        self.speed = 10
        self.speed_player = 10


        self.reset()
        # self.player()




    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

        self.direction1 = Direction.RIGHT

        self.head_player = Point(self.w/2, self.h/2)
        self.snake_player = [self.head_player,
                      Point(self.head_player.x-BLOCK_SIZE, self.head_player.y),
                      Point(self.head_player.x-(2*BLOCK_SIZE), self.head_player.y)]

        self.score_player = 0
        self.food_player = None
        self._place_food_player()
        self.frame_iteration = 0

    # def player(self):
    #     # init game state
    #     self.direction1 = Direction.RIGHT
    #
    #     self.head_player = Point(self.w/2, self.h/2)
    #     self.snake_player = [self.head_player,
    #                   Point(self.head_player.x-BLOCK_SIZE, self.head_player.y),
    #                   Point(self.head_player.x-(2*BLOCK_SIZE), self.head_player.y)]
    #
    #     self.score_player = 0
    #     self.food_player = None
    #     self._place_food_player()
    #     self.frame_iteration = 0


    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def _place_food_player(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food_player = Point(x, y)
        if self.food_player in self.snake_player:
            self._place_food_player()


    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction1 != Direction.RIGHT:
                    self.direction1 = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction1 != Direction.LEFT:
                    self.direction1 = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction1 != Direction.DOWN:
                    self.direction1 = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction1 != Direction.UP:
                    self.direction1 = Direction.DOWN

        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)

        self.move_player(self.direction1)
        self.snake_player.insert(0, self.head_player)



        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake) or self.is_collision_player():
            game_over = True
            reward = -10
            # self.display.fill((202, 228, 241))
            return reward, game_over, self.score


        # if self.is_collision_player():
        #     game_over = True
        #     # reward = -10
        #     # return reward, game_over, self.score


        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        if self.head_player == self.food_player:
            self.speed_player +=1
            self.score_player += 1
            self._place_food_player()
        else:
            self.snake_player.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(self.speed_player)
        # self.clock_player.tick(self.speed_player)
        # 6. return game over and score
        return reward, game_over, self.score


    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False

    def is_collision_player(self):
        # hits boundary
        if self.head_player.x > self.w - BLOCK_SIZE or self.head_player.x < 0 or self.head_player.y > self.h - BLOCK_SIZE or self.head_player.y < 0:
            return True
        # hits itself
        if self.head_player in self.snake_player[1:]:
            return True
        return False


    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))


        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        for pt in self.snake_player:
            pygame.draw.rect(self.display, GREEN2, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            # pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, PINK, pygame.Rect(self.food_player.x, self.food_player.y, BLOCK_SIZE, BLOCK_SIZE))


        text = font.render("Score: " + str(self.score), True, WHITE)
        text1 = font.render("Score: " + str(self.score_player), True, WHITE)

        self.display.blit(text, [0, 0])
        self.display.blit(text1, [300, 0])
        pygame.display.flip()


    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

    def move_player(self, direction):
        x = self.head_player.x
        y = self.head_player.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE  # Move by double the distance
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE  # Move by double the distance
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE  # Move by double the distance
        elif direction == Direction.UP:
            y -= BLOCK_SIZE  # Move by double the distance

        self.head_player = Point(x, y)

    # def pause_game(self):
    #     paused = True
    #     while paused:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 quit()
    #             if event.type == pygame.KEYDOWN:
    #                 if event.key == pygame.K_SPACE:
    #                     paused = False
    #
    #         # Display "Paused" message
    #         text = font.render("Paused", True, WHITE)
    #         self.display.blit(text, [self.w // 2 - 50, self.h // 2 - 25])
    #
    #         # Add buttons
    #         button_font = pygame.font.Font('arial.ttf', 20)
    #         resume_text = button_font.render("Resume", True, WHITE)
    #         quit_text = button_font.render("Quit", True, WHITE)
    #
    #         resume_button_rect = resume_text.get_rect(center=(self.w // 2, self.h // 2 + 25))
    #         quit_button_rect = quit_text.get_rect(center=(self.w // 2, self.h // 2 + 75))
    #
    #         pygame.draw.rect(self.display, GREEN1, resume_button_rect)
    #         pygame.draw.rect(self.display, GREEN1, quit_button_rect)
    #
    #         self.display.blit(resume_text, resume_button_rect)
    #         self.display.blit(quit_text, quit_button_rect)
    #
    #         pygame.display.update()
    #         self.clock.tick(5)  # Adjust the frame rate



