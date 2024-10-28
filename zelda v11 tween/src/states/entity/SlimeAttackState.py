import random
import math
from src.states.BaseState import BaseState
from src.HitBox import Hitbox
import pygame

class SlimeAttackState(BaseState):
    def __init__(self, slime, dungeon=None):
        self.slime = slime
        self.dungeon = dungeon
        self.attack_delay = 3.0  # Delay between attacks in seconds
        self.attack_timer = 0
        self.is_attacking = False
        self.slime.is_attacked = False
        # Four hitboxes for each direction
        self.hitboxes = {
            "left": None,
            "right": None,
            "up": None,
            "down": None,
        }

    def Enter(self, params):
        print('Slime preparing to attack in all directions')
        # Reset attack timer and flags
        self.attack_timer = 0
        self.is_attacking = True
        self.slime.is_attacked = False

        # Create hitboxes for all directions
        self.hitboxes["left"] = self.create_hitbox("left")
        self.hitboxes["right"] = self.create_hitbox("right")
        self.hitboxes["up"] = self.create_hitbox("up")
        self.hitboxes["down"] = self.create_hitbox("down")

    def ProcessAI(self, params, dt):
        if self.is_attacking:
            self.attack_timer += dt
            if self.attack_timer >= self.attack_delay:
                print('Slime attack complete, returning to walk state')
                self.is_attacking = False
                self.slime.ChangeState("walk")

    def update(self, dt, events):
        if self.is_attacking:
            # Update hitbox positions relative to the slime's current position
            self.hitboxes["left"].x = self.slime.rect.x - 300
            self.hitboxes["right"].x = self.slime.rect.x + self.slime.width
            self.hitboxes["up"].y = self.slime.rect.y - 300
            self.hitboxes["down"].y = self.slime.rect.y + self.slime.height

    def create_hitbox(self, direction):
        if direction == "left":
            return Hitbox(self.slime.rect.x - 300, self.slime.rect.y + 6, 300, 48)
        elif direction == "right":
            return Hitbox(self.slime.rect.x + self.slime.width, self.slime.rect.y + 6, 300, 48)
        elif direction == "up":
            return Hitbox(self.slime.rect.x, self.slime.rect.y - 300, 48, 300)
        elif direction == "down":
            return Hitbox(self.slime.rect.x, self.slime.rect.y + self.slime.height, 48, 300)

    def render(self, screen):
        animation = self.slime.curr_animation.image
        screen.blit(animation, (math.floor(self.slime.rect.x - self.slime.offset_x),
                                math.floor(self.slime.rect.y - self.slime.offset_y)))
        # Draw each hitbox for all four directions
        for direction, hitbox in self.hitboxes.items():
            if hitbox:
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(hitbox.x, hitbox.y, hitbox.width, hitbox.height), 2)

    def Exit(self):
        print('Exiting SlimeAttackState')
        # Clear hitboxes and reset attacking flag
        self.hitboxes = { "left": None, "right": None, "up": None, "down": None }
        self.is_attacking = False
        self.slime.is_attacked = True



