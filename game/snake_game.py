import pygame
import random
from collections import namedtuple

# RGB colors
BLACK = (0, 0, 0)
RED = (200, 0, 0)
WHITE = (255, 255, 255)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)

BLOCK_SIZE = 20
SPEED = 20
Point = namedtuple('Point', 'x, y')

pygame.init()