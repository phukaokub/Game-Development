import pygame
import math
from src.constants import *
from src.Dependency import *

class PenBall:
    def __init__(self, x, y, dx, dy, level):
        print("PenBall")
        self.width = 8
        self.height = 8
        
        self.x = x
        self.y = y
        self.dx = dx/2
        self.dy = dy/2
        self.type = 0

        print(f'self.x: {self.x}')
        print(f'self.y: {self.y}')
        print(f'self.dx: {self.dx}')
        print(f'self.dy: {self.dy}')

        self.time = 1 + (math.floor(level * 1.5) % 5)
        self.alive = True

        self.image = ball_image_list[5]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def Collides(self, target):
        if self.rect.x > target.rect.x + target.width or target.rect.x >self.rect.x + self.width:
            return False

        if self.rect.y > target.rect.y + target.height or target.rect.y > self.rect.y + self.height:
            return False

        return True

    def update(self, dt):
        self.time -= dt
        if self.time <= 0:
            self.alive = False
        self.rect.x += self.dx * dt
        self.rect.y += self.dy * dt

        #A ball hits a left wall
        if self.rect.x <= 0:
            self.rect.x = 0
            self.dx = -self.dx
            gSounds['wall-hit'].play()

        # A ball hits a right wall
        if self.rect.x >= WIDTH - 24:
            self.rect.x = WIDTH - 24
            self.dx = -self.dx
            gSounds['wall-hit'].play()

        # A ball hits a upper wall
        if self.rect.y <= 0:
            self.rect.y = 0
            self.dy = -self.dy
            gSounds['wall-hit'].play()

    def render(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))