import random

from src.states.BaseState import BaseState
from src.constants import *

class EntityWalkState(BaseState):
    def __init__(self, entity, dungeon=None):
        self.entity = entity
        self.entity.ChangeAnimation('down')
        self.dungeon = dungeon

        #AI control
        self.move_duration = 0
        self.movement_timer = 0

        #hit wall?
        self.bumped = False

    def update(self, dt, events):
        self.bumped=False

        if self.entity.direction == "left":
            self.entity.MoveX(-self.entity.walk_speed*dt)
            if self.entity.rect.x <= MAP_RENDER_OFFSET_X + TILE_SIZE:
                #self.entity.rect.x = MAP_RENDER_OFFSET_X + TILE_SIZE
                self.entity.ChangeCoord(x=MAP_RENDER_OFFSET_X + TILE_SIZE)
                self.bumped=True
        elif self.entity.direction == "right":
            self.entity.MoveX(self.entity.walk_speed * dt)
            if self.entity.rect.x + self.entity.width >= WIDTH - TILE_SIZE * 2:
                #self.entity.rect.x = WIDTH - TILE_SIZE * 2 - self.entity.width
                self.entity.ChangeCoord(x=WIDTH - TILE_SIZE * 2 - self.entity.width)
                self.bumped=True

        elif self.entity.direction == 'up':
            self.entity.MoveY(-self.entity.walk_speed * dt)
            if self.entity.rect.y <= MAP_RENDER_OFFSET_Y + TILE_SIZE - self.entity.height /2:
                #self.entity.rect.y = MAP_RENDER_OFFSET_Y + TILE_SIZE - self.entity.height /2
                self.entity.ChangeCoord(y=MAP_RENDER_OFFSET_Y + TILE_SIZE - self.entity.height /2)
                self.bumped = True

        elif self.entity.direction == 'down':
            self.entity.MoveY(self.entity.walk_speed * dt)
            bottom_edge = HEIGHT - (HEIGHT - MAP_HEIGHT * TILE_SIZE) + MAP_RENDER_OFFSET_Y - TILE_SIZE
            if self.entity.rect.y + self.entity.height >= bottom_edge:
                #self.entity.rect.y = bottom_edge-self.entity.height
                self.entity.ChangeCoord(y=bottom_edge-self.entity.height)
                self.bumped=True

        #print(self.entity.rect.x, self.entity.rect.y, self.entity.walk_speed*dt)

    def Enter(self, params):
        pass
    def Exit(self):
        pass

    def ProcessAI(self, params, dt):
        directions = ['left', 'right', 'up', 'down']

        if self.move_duration == 0 or self.bumped:
            self.move_duration = random.randint(0, 5)
            self.entity.direction = random.choice(directions)
            self.entity.ChangeAnimation(self.entity.direction)

        elif self.movement_timer > self.move_duration:
            self.movement_timer = 0
            if random.randint(0, 3) == 1:
                self.entity.ChangeState('idle')
            else:
                self.move_duration = random.randint(0, 5)
                self.entity.direction = random.choice(directions)
                self.entity.ChangeAnimation(self.entity.direction)

        self.movement_timer = self.movement_timer+dt


    def render(self, screen):
        animation = self.entity.curr_animation.image

        screen.blit(animation, (math.floor(self.entity.rect.x - self.entity.offset_x),
                    math.floor(self.entity.rect.y - self.entity.offset_y)))