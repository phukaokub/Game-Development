import math

from src.states.BaseState import BaseState
from src.HitBox import Hitbox
import pygame
from src.recourses import *

class PlayerLiftingState(BaseState):
    def __init__(self, player, dungeon=None):
        self.player = player
        self.dungeon = dungeon

        self.player.curr_animation.Refresh()
        self.player.ChangeAnimation("lift_"+self.player.direction)


    def Enter(self, params):
        #sounds
        direction = self.player.direction

        if direction == 'left':
            hitbox_width = 24
            hitbox_height = 48
            hitbox_x = self.player.x - hitbox_width
            hitbox_y = self.player.y + 6
        elif direction == 'right':
            hitbox_width = 24
            hitbox_height = 48
            hitbox_x = self.player.x + self.player.width
            hitbox_y = self.player.y + 6
        elif direction == 'up':
            hitbox_width = 48
            hitbox_height = 24
            hitbox_x = self.player.x
            hitbox_y = self.player.y - hitbox_height
        elif direction == 'down':
            hitbox_width = 48
            hitbox_height = 24
            hitbox_x = self.player.x
            hitbox_y = self.player.y + self.player.height

        self.lifting_hitbox = Hitbox(hitbox_x, hitbox_y, hitbox_width, hitbox_height)

        self.player.ChangeAnimation("lift_"+self.player.direction)

    def Exit(self):
        pass

    def update(self, dt, events):
        for object in self.dungeon.current_room.objects:
            if self.player.Collides(object) and object.type == 'pot':
                gSounds['hit_enemy'].play()
                self.dungeon.current_room.objects.remove(object)

        if self.player.curr_animation.times_played > 0:
            self.player.curr_animation.times_played = 0
            self.player.ChangeState("idle")  #check

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    print("lift")
                    self.player.ChangeState('lift')


    def render(self, screen):
        animation = self.player.curr_animation.image
        screen.blit(animation, (math.floor(self.player.x - self.player.offset_x), math.floor(self.player.y - self.player.offset_y)))

        #hit box debug
        #pygame.draw.rect(screen, (255, 0, 255), pygame.Rect(self.sword_hitbox.x, self.sword_hitbox.y, self.sword_hitbox.width, self.sword_hitbox.height))