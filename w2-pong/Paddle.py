import pygame
import random
from constant import *

class Paddle:
    def __init__(self, screen, x, y, width, height, color, neon_color):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.dy = 0
        self.speed = PADDLE_SPEED
        self.color = color
        self.neon_color = neon_color
        self.radius = 10  # Radius for rounded corners
        self.border_thickness = 5  # Thickness of the neon border

    def update(self, dt):
        self.rect.y += self.dy * dt
        self.rect.y = max(min(self.rect.y, HEIGHT - self.rect.height), 0)  # Ensure paddle stays within bounds

    def render(self):
        # Draw the neon border
        self._draw_neon_border()

        # Draw the paddle body with blank fill
        pygame.draw.rect(self.screen, self.color, self.rect)

    def _draw_neon_border(self):
        # Draw the neon border
        neon_rect = pygame.Rect(self.rect.x - self.border_thickness, self.rect.y - self.border_thickness,
                                self.rect.width + 2 * self.border_thickness, self.rect.height + 2 * self.border_thickness)
        neon_surface = pygame.Surface((neon_rect.width, neon_rect.height), pygame.SRCALPHA)

        # Draw the rounded rectangle for the neon border
        pygame.draw.rect(neon_surface, self.neon_color, neon_surface.get_rect(), border_radius=self.radius)
        pygame.draw.rect(neon_surface, self.neon_color, (0, 0, neon_rect.width, neon_rect.height), border_radius=self.radius, width=self.border_thickness)

        self.screen.blit(neon_surface, (neon_rect.x, neon_rect.y))

    def predictive_AI(self, ball, dt, reaction_speed):
        # Margin from the edge of the paddle where collision happens
        COLLISION_MARGIN = 10  # Adjust this value as needed

        if ball.dx == 0:
            return  # Avoid division by zero

        # Randomly decide whether to follow the real or fake ball
        if ball.fake_ball and random.random() < 0.5:
            target_ball = ball.fake_ball
            self.following_real_ball = False
        else:
            target_ball = ball
            self.following_real_ball = True

        # Calculate the x position where the ball will collide with the paddle
        if target_ball.dx > 0:
            collision_x = WIDTH - COLLISION_MARGIN
        else:
            collision_x = COLLISION_MARGIN

        # Calculate time for the ball to reach the collision_x
        time_to_collision_x = (collision_x - target_ball.rect.x) / target_ball.dx
        predicted_y = target_ball.rect.y + target_ball.dy * time_to_collision_x

        # Ensure the predicted position is within screen bounds
        predicted_y = max(min(predicted_y, HEIGHT - self.rect.height), 0)

        # Move paddle towards the predicted y position
        if self.rect.centery < predicted_y:
            self.dy = self.speed * reaction_speed
        else:
            self.dy = -self.speed * reaction_speed

        # If the fake ball disappears, switch back to following the real ball
        if not ball.fake_ball:
            self.following_real_ball = True

    def strong_AI(self, ball, dt):
        # Strong AI: faster reaction speed
        self.neon_color = (51, 204, 51)
        self.predictive_AI(ball, dt, reaction_speed=1.0)

    def weak_AI(self, ball, dt):
        # Weak AI: slower reaction speed
        self.neon_color = (204, 255, 204)
        self.predictive_AI(ball, dt, reaction_speed=0.5)
        
    def reduce_paddle_size(self):
        self.rect.height -= 10

    def increase_paddle_size(self):
        self.rect.height += 10

    def reset_paddle_size(self):
        self.rect.height = 60  # Reset the paddle's size to the original value