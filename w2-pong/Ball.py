import pygame
import random
from constant import *

class Ball:
    def __init__(self, screen, x, y, width, height, color):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.dx = random.choice([-300, 300])
        self.dy = random.randint(-150, 150)
        self.color = color
        self.is_fake = False 
        self.fake_ball = None  
        self.activate_mirror = None

        self.small_font = pygame.font.Font('w2-pong/font.ttf', 24)
        self.large_font = pygame.font.Font('w2-pong/font.ttf', 48)
        self.score_font = pygame.font.Font('w2-pong/font.ttf', 96)

    def Collides(self, paddle):
        if self.rect.x > paddle.rect.x + paddle.rect.width or paddle.rect.x > self.rect.x + self.rect.width:
            return False
        if self.rect.y > paddle.rect.y + paddle.rect.height or paddle.rect.y > self.rect.y + self.rect.height:
            return False
        return True

    def Reset(self):
        self.rect.x = WIDTH / 2 - 6
        self.rect.y = HEIGHT / 2 - 6
        self.dx = 0
        self.dy = 0
        self.is_fake = False  
        self.fake_ball = None  # Remove the fake ball

    def update(self, dt):
        self.rect.x += self.dx * dt
        self.rect.y += self.dy * dt

        # Handle fake ball update
        if self.fake_ball:
            self.fake_ball.rect.x += self.fake_ball.dx * dt
            self.fake_ball.rect.y += self.fake_ball.dy * dt

            # Remove the fake ball if it crosses the halfway point
            if (self.dx > 0 and self.fake_ball.rect.x > WIDTH / 2) or (self.dx < 0 and self.fake_ball.rect.x < WIDTH / 2):
                self.fake_ball = None

    def render(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

        # Render the fake ball if it exists
        if self.fake_ball:
            pygame.draw.rect(self.screen, (255, 255, 255), self.fake_ball.rect)  # Gray color for fake ball

    def activate_mirror_ball(self):
        # Create a fake ball with the same position and movement as the real ball
        self.fake_ball = Ball(self.screen, self.rect.x, self.rect.y, self.rect.width, self.rect.height, (0, 255, 255))
        direction = random.randint(0, 1)
        if direction == 0:
            self.fake_ball.dy = -self.dy
        else:
            self.fake_ball.dy = self.dy
            self.dy = -self.dy
        self.fake_ball.dx = self.dx
        self.is_fake = False

    def receive_mirror_ball(self, paddle):
        self.activate_mirror = paddle
        self.is_fake = True
        self.fake_ball = None

    def activate_speed_ball(self):
        self.color = (255, 0, 0)
        self.dx *= 1.2
        self.dy *= 1.2
    
    def reset_color(self):
        self.color = (255, 255, 255)

    
