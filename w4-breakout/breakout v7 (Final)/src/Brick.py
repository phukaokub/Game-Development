import pygame
from src.Dependency import *
from src.PenBall import PenBall
from src.Explode import Explode
import random

class Brick:
    def __init__(self, x, y):
        self.tier = 0  # n -> 0
        self.color = 1  # 5 -> 1

        self.x = x
        self.y = y

        self.width = 96
        self.height = 48

        self.alive = True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def Hit(self, paddle, ball):
        powerup = None
        penBall = None
        explosion = None
        
        if ball.type == 0:
            gSounds['brick-hit2'].play()
        elif ball.type == 1:
            gSounds['explosion'].play()
            ball.type = 0
            explosion = Explode(ball.rect.x + ball.rect.width // 2, ball.rect.y + ball.rect.height // 2, radius=100)
        elif ball.type == 2:
            penBall = PenBall(ball.rect.x, ball.rect.y, ball.dx, ball.dy, paddle.item3_level)
            ball.type = 0

        # Calculate damage based on paddle's item1_level
        damage = paddle.item1_level % 4 + 1
        
        # Apply damage to the brick's tier and color
        total_health = self.tier * 5 + self.color  # Convert tier and color into a single health pool
        total_health -= damage  # Reduce health by the damage value
        
        # Update the brick's tier and color based on remaining health
        if total_health > 0:
            self.tier = total_health // 5  # Calculate new tier
            self.color = total_health % 5  # Calculate new color
            
            if self.color == 0 and self.tier > 0:  # Handle edge case for tier change when color is 0
                self.tier -= 1
                self.color = 5
        else:
            self.alive = False  # The brick is destroyed
        
        # Play sound based on brick's state
        if not self.alive:
            gSounds['brick-hit1'].play()
        
        # Process power-ups
        if paddle.item2_level >= 1 and self.spawnChance(paddle.item2_level):
            powerup = self.spawnPowerup("bomb")
        if paddle.item3_level >= 1 and self.spawnChance(paddle.item3_level):
            powerup = self.spawnPowerup("penetrate")
        
        return powerup, penBall, explosion

    def update(self, dt):
        pass

    def render(self, screen):
        if self.alive:
            screen.blit(brick_image_list[((self.color - 1) * 4) + self.tier], (self.rect.x, self.rect.y))

    def spawnChance(self, level):
        base_chance = 20
        additional_chance = (level // 5) * 5
        spawn_chance = base_chance + additional_chance
        roll = random.randint(1, 100)
        return roll <= spawn_chance

    def spawnPowerup(self, powerup_type):
        if powerup_type == "bomb":
            powerup = 0
        elif powerup_type == "penetrate":
            powerup = 1
        return PowerUp(self.rect.x, self.rect.y, powerup)
