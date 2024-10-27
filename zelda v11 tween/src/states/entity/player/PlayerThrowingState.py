import math
from src.states.BaseState import BaseState
from src.HitBox import Hitbox
import pygame
from src.recourses import *

class PlayerThrowingState(BaseState):
    def __init__(self, player, dungeon=None):
        self.player = player
        self.dungeon = dungeon
        self.pot_hitbox = None  # Hitbox for the pot

    def Enter(self, params):
        # Sounds
        print('throwing')
        self.player.is_lift = False
        direction = self.player.direction
        throw_speed = 5  # Set the throw speed

        # Set the object's direction and velocity for throwing
        if hasattr(self.player, 'carrying_object'):
            self.player.carrying_object.throw(direction, throw_speed)
            self.pot_hitbox = self.create_hitbox(direction)
            self.player.carrying_object = None

        # Set animation
        self.player.ChangeAnimation("throw_" + direction)

    def create_hitbox(self, direction):
        if direction == 'left':
            hitbox_width = 300
            hitbox_height = 48
            hitbox_x = self.player.x - hitbox_width
            hitbox_y = self.player.y + 6
        elif direction == 'right':
            hitbox_width = 300
            hitbox_height = 48
            hitbox_x = self.player.x + self.player.width
            hitbox_y = self.player.y + 6
        elif direction == 'up':
            hitbox_width = 48
            hitbox_height = 300
            hitbox_x = self.player.x
            hitbox_y = self.player.y - hitbox_height
        elif direction == 'down':
            hitbox_width = 48
            hitbox_height = 300
            hitbox_x = self.player.x
            hitbox_y = self.player.y + self.player.height

        return Hitbox(hitbox_x, hitbox_y, hitbox_width, hitbox_height)

    def Exit(self):
        pass

    def update(self, dt, events):
        # Update the pot's position and check for collisions
        if self.player.carrying_object and self.player.carrying_object.is_thrown:
            self.pot_hitbox.x = self.player.carrying_object.x
            self.pot_hitbox.y = self.player.carrying_object.y

        # Check if the throwing animation has completed
        if self.player.curr_animation.times_played > 0:
            self.player.curr_animation.times_played = 0
            self.player.ChangeState("idle")

    def render(self, screen):
        animation = self.player.curr_animation.image
        screen.blit(animation, (math.floor(self.player.x - self.player.offset_x), math.floor(self.player.y - self.player.offset_y)))

        # Hitbox debug (optional)
        # pygame.draw.rect(screen, (255, 0, 255), pygame.Rect(self.pot_hitbox.x, self.pot_hitbox.y, self.pot_hitbox.width, self.pot_hitbox.height))