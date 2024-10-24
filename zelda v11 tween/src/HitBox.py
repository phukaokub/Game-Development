import pygame

class Hitbox:
    def __init__(self, x, y, width, height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)