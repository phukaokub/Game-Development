import pygame
from src.Dependency import *

class Brick:
    def __init__(self, x, y):
        self.tier=0   #n->0
        self.color=1  #5->1

        self.x=x
        self.y=y

        self.width = 96
        self.height = 48

        self.alive = True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def Hit(self):
        gSounds['brick-hit2'].play()
        self.alive=False

    def update(self, dt):
        pass

    def render(self, screen):
        if self.alive:
            screen.blit(brick_image_list[((self.color-1)*4)+self.tier], (self.rect.x, self.rect.y))