import pygame
import random
from src.constants import *
from src.resources import *

class PowerUp:
    def __init__(self, x, y, powerup_type):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.dy = 100  # Falling speed of powerup
        self.type = powerup_type
        self.alive = True
        
        # Select image based on the powerup type
        self.image = powerup_image_list[self.type]  # Use appropriate image for powerup type

        # Create a rectangle for collision detection
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, dt):
        # Update the powerup position, making it fall downwards
        self.rect.y += self.dy * dt

        # Despawn the powerup if it goes off the bottom of the screen
        if self.rect.y > HEIGHT:
            self.alive = False

    def render(self, screen):
        # Render the powerup on the screen
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def check_collision_with_paddle(self, paddle):
        # Check if the powerup collides with the paddle
        if self.rect.colliderect(paddle.rect):
            self.alive = False  # Powerup is consumed
            return True

