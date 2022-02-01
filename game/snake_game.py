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

    def _place_food(self) -> None:
        x = random.randint(0, (self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.height-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def step(self) -> tuple[bool, int]:
        # user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.direction = DirectionEnum.RIGHT
                elif event.key == pygame.K_LEFT:
                    self.direction = DirectionEnum.LEFT
                elif event.key == pygame.KEYDOWN:
                    self.direction = DirectionEnum.DOWN
                elif event.key == pygame.KEYUP:
                    self.direction = DirectionEnum.UP

        # move - snake head update
        self._move(self.direction)
        self.snake.insert(0, self.head)

        # game over condition
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # collect food or move tail
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        return game_over, self.score

    def _is_collision(self):
        pass

    def _update_ui(self):
        pass

    def _move(self, direction: DirectionEnum) -> None:
        x = self.head.x
        y = self.head.y

        if direction == DirectionEnum.RIGHT:
            x += BLOCK_SIZE
        elif direction == DirectionEnum.LEFT:
            x -= BLOCK_SIZE
        elif direction == DirectionEnum.DOWN:
            y += BLOCK_SIZE
        elif direction == DirectionEnum.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)
