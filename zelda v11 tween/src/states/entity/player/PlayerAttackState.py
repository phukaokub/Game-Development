import math

from src.states.BaseState import BaseState
from src.HitBox import Hitbox
import pygame
from src.recourses import *

class PlayerAttackState(BaseState):
    def __init__(self, player, dungeon=None):
        self.player = player
        self.dungeon = dungeon

        self.player.curr_animation.Refresh()
        self.player.ChangeAnimation("attack_"+self.player.direction)


    def Enter(self, params):
        #sounds
        self.player.offset_x = 24
        self.player.offset_y = 15

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

        self.sword_hitbox = Hitbox(hitbox_x, hitbox_y, hitbox_width, hitbox_height)

        self.player.curr_animation.Refresh()
        print(self.player.curr_animation.index)
        self.player.ChangeAnimation("attack_"+self.player.direction)

    def Exit(self):
        pass

    def update(self, dt, events):
        for entity in self.dungeon.current_room.entities:
            if entity.Collides(self.sword_hitbox) and not entity.invulnerable:
                entity.Damage(1)
                entity.SetInvulnerable(0.2)
                gSounds['hit_enemy'].play()

        if self.player.curr_animation.times_played > 0:
            self.player.curr_animation.times_played = 0
            self.player.ChangeState("idle")  #check

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.ChangeState('swing_sword')


    def render(self, screen):
        animation = self.player.curr_animation.image
        screen.blit(animation, (math.floor(self.player.x - self.player.offset_x), math.floor(self.player.y - self.player.offset_y)))

        #hit box debug
        #pygame.draw.rect(screen, (255, 0, 255), pygame.Rect(self.sword_hitbox.x, self.sword_hitbox.y, self.sword_hitbox.width, self.sword_hitbox.height))