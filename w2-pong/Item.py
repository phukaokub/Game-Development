import pygame
import random
from constant import *

class Item:
    def __init__(self, screen, x, y, item_type):
        self.screen = screen
        self.rect = pygame.Rect(x, y, ITEM_WIDTH, ITEM_HEIGHT)
        self.item_type = item_type
        self.color = self.get_color()
        self.font = pygame.font.Font(None, 24)
        
    def get_color(self):
        if self.item_type == 'mirror_ball':
            return (0, 255, 255)  # Cyan
        elif self.item_type == 'speed_ball':
            return (255, 0, 0)    # Red
        elif self.item_type == 'reduce_paddle_size':
            return (255, 165, 0)  # Orange
        elif self.item_type == 'increase_paddle_size':
            return (255, 255, 0) # Yellow

    def render(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        self.render_text()

    def render_text(self):
        text_surface = self.font.render(self.item_type, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.y - 10))
        self.screen.blit(text_surface, text_rect)

    def activate(self, ball, paddle1, paddle2):
        if self.item_type == 'mirror_ball':
            if ball.dx > 0:
                paddle_to_react = paddle1
            else:
                paddle_to_react = paddle2
            ball.receive_mirror_ball(paddle_to_react)
        elif self.item_type == 'speed_ball':
            ball.activate_speed_ball()
        elif self.item_type == 'reduce_paddle_size':
            # Check which paddle to reduce based on the ball's direction
            if ball.dx > 0:  # Ball is moving towards the right
                paddle_to_reduce = paddle2
            else:  # Ball is moving towards the left
                paddle_to_reduce = paddle1

            # Reduce the size of the determined paddle
            paddle_to_reduce.reduce_paddle_size()
        elif self.item_type == 'increase_paddle_size':
            # Check which paddle to increase based on the ball's direction
            if ball.dx > 0:
                paddle_to_increase = paddle1
            else:
                paddle_to_increase = paddle2

            # Increase the size of the determined paddle
            paddle_to_increase.increase_paddle_size()

    def update(self, ball, paddle1, paddle2):
        if self.rect.colliderect(ball.rect):
            self.activate(ball, paddle1, paddle2)  # Pass the ball and both paddles
            return True  # Indicate that the item has been consumed
        return False  # Item is still active

