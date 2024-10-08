import pygame
import random
from src.constants import *

class Explode:
    def __init__(self, x, y, radius=100):
        self.x = x
        self.y = y
        self.radius = radius
        self.time_to_live = 0.5  # seconds
        self.start_time = pygame.time.get_ticks()
        self.image = pygame.Surface((radius * 2, radius * 2))
        self.image.set_alpha(128)
        self.image.fill((255, 255, 255))  # White color for explosion

    def update(self, dt):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000.0
        if elapsed_time > self.time_to_live:
            return False  # Explosion should be removed after its lifetime
        return True

    def render(self, screen):
        if self.update(0):
            # Draw explosion as a circle on the screen
            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)
        else:
            return False  # No need to render if explosion is done
        return True

    def is_within_radius(self, x, y):
        """ Check if a point is within the explosion radius. """
        distance = ((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5
        return distance <= self.radius
