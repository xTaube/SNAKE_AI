import pygame
import random
from collections import namedtuple
from game.direction import DirectionEnum
import numpy as np

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
pygame.font.init()
font = pygame.font.SysFont('arial', 25)


class SnakeGame:

    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height

        # init display
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

        self._reset()

    def play(self) -> None:
        while True:
            _, game_over, score = self._step()
            if game_over:
                break

        print(f'Final score {score}')

        pygame.quit()
        exit()

    def _reset(self) -> None:
        # init game state
        self.direction = DirectionEnum.RIGHT
        self.head = Point(self.width / 2, self.height / 2)
        self.snake = [self.head, Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - 2 * BLOCK_SIZE, self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iterations = 0

    def _step(self) -> tuple[int, bool, int]:
        self.frame_iterations += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # move - snake head update
        self._move(action)
        self.snake.insert(0, self.head)

        # game over condition
        reward = 0
        game_over = False
        if self._is_collision() or self.frame_iterations > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # collect food or move tail
        if self.head == self.food:
            reward = 10
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        return reward, game_over, self.score

    def _place_food(self) -> None:
        x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def _is_collision(self, pt=None) -> bool:
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.width - BLOCK_SIZE \
                or pt.x < 0 \
                or pt.y > self.height - BLOCK_SIZE \
                or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False

    def _update_ui(self) -> None:
        self.display.fill(BLACK)

        for body_part in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(body_part.x, body_part.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(body_part.x + 4, body_part.y + 4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        score_text = font.render(f'Score: {self.score}', True, WHITE)
        self.display.blit(score_text, [0, 0])
        pygame.display.flip()

    def _move(self, action: list) -> None:
        # [straight, right, left]
        clock_wise = [DirectionEnum.RIGHT, DirectionEnum.DOWN, DirectionEnum.LEFT, DirectionEnum.UP]
        idx = clock_wise.index(self.direction)
        new_dir = None
        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4    # turn right
            new_dir = clock_wise[next_idx]
        elif np.array_equal(action, [0, 0, 1]):
            next_idx = (idx - 1) % 4    # turn left
            new_dir = clock_wise[next_idx]

        self.direction = new_dir

        x = self.head.x
        y = self.head.y

        if self.direction == DirectionEnum.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == DirectionEnum.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == DirectionEnum.DOWN:
            y += BLOCK_SIZE
        elif self.direction == DirectionEnum.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)
