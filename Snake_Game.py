import pygame
import sys
import time
import random

from pygame.locals import *

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = WINDOW_WIDTH / GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT / GRID_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (250, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

FPS = 60


class Python(object):
    def __init__(self):
        self.create()
        self.color = WHITE
        self.attempt = 0

    def create(self):
        self.length = 2
        self.positions = [(((WINDOW_WIDTH / GRID_SIZE)//2) * GRID_SIZE, ((WINDOW_HEIGHT / GRID_SIZE)//2) * GRID_SIZE)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        

    def control(self, xy):
        if (xy[0] * -1, xy[1] * -1) == self.direction:
            return
        else:
            self.direction = xy

    def move(self):
        cur = self.positions[0]
        x, y = self.direction
        new = (cur[0] + (x * GRID_SIZE), cur[1] + (y * GRID_SIZE))
        if new in self.positions[2:]:
            self.create()
            self.attempt += 1
            
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
        if ((new[0] >= WINDOW_WIDTH) | (new[0] < 0)):
            self.create()
            self.attempt += 1
        if ((new[1] >= WINDOW_HEIGHT) | (new[1] < 0)):
            self.create()
            self.attempt += 1
        
        

    def eat(self):
        self.length += 1

    def get_length(self):
        return self.length
        
        

    def draw(self, surface):
        for p in self.positions:
            draw_object(surface, self.color, p)

    def score(self, surface):
        self.font = pygame.font.SysFont("freesansbold.ttf", 30, True)
        # This should go inside the redrawGameWindow function
        self.text = self.font.render("Score: " + str(self.length - 2) + "  Attempt: " + str(self.attempt), 3, (255,255,255)) # Arguments are: text, anti-aliasing, color
        surface.blit(self.text, ((WINDOW_WIDTH) - self.text.get_width(), self.text.get_height()))


class Feed(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.create()

    def create(self):
         self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
         while self.position in python.positions:
             self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
    
    def draw(self, surface):
        draw_object(surface, self.color, self.position)



def draw_object(surface, color, pos):
    r = pygame.Rect((pos[0], pos[1] ), (GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(surface, color, r)

def check_eat(python, feed):
    if python.positions[0] == feed.position:
        python.eat()
        if python.length == ((WINDOW_WIDTH // GRID_SIZE) * (WINDOW_HEIGHT // GRID_SIZE) + 1):
            python.create()
        feed.create()
    return python.get_length()


if __name__ == '__main__':
    python = Python()
    feed = Feed()

    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
    pygame.display.set_caption('Python Game')
    surface = pygame.Surface(window.get_size())
    surface = surface.convert()
    surface.fill(BLACK)
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 40)
    window.blit(surface, (0, 0))

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    python.control(UP)
                elif event.key == K_DOWN:
                    python.control(DOWN)
                elif event.key == K_LEFT:
                    python.control(LEFT)
                elif event.key == K_RIGHT:
                    python.control(RIGHT)
        
        surface.fill(BLACK)
        python.move()
        SCORE = check_eat(python, feed)
        speed = (FPS + python.length) / 5
        python.draw(surface)
        feed.draw(surface)
        python.score(surface)
        window.blit(surface, (0, 0))
        pygame.display.flip()
        pygame.display.update()
        clock.tick(speed)

# Change Check 222222