import pygame
import random
from collections import namedtuple
from direction import DirectionEnum

# RGB colors
BLACK = (0, 0, 0)
RED = (200, 0, 0)
WHITE = (255, 255, 255)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)

# Static variables
BLOCK_SIZE = 20
SPEED = 20
Point = namedtuple('Point', 'x, y')

pygame.init()


class SnakeGame:

    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height

        # init display
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

        # init game state
        self.direction = DirectionEnum.RIGHT
        self.head = Point(self.width/2, self.height/2)
        self.snake = [self.head, Point(self.head.x-BLOCK_SIZE, self.head.y), Point(self.head.x-2*BLOCK_SIZE)]
        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        pass

    def _play_step(self):
        pass

    def _is_collision(self):
        pass

    def _update_ui(self):
        pass

    def _move(self):
        pass
