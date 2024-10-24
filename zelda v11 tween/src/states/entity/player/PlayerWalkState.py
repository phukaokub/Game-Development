from src.constants import *
from src.states.entity.EntityWalkState import EntityWalkState
import pygame, time

class PlayerWalkState(EntityWalkState):
    def __init__(self, player, dungeon):
        super(PlayerWalkState, self).__init__(player, dungeon)

        self.entity.ChangeAnimation('down')
        self.dungeon = dungeon

    def Exit(self):
        pass

    def Enter(self, params):
        self.entity.offset_y = 15
        self.entity.offset_x = 0

    def update(self, dt, events):
        pressedKeys = pygame.key.get_pressed()
        if pressedKeys[pygame.K_LEFT]:
            self.entity.direction = 'left'
            self.entity.ChangeAnimation('left')
        elif pressedKeys[pygame.K_RIGHT]:
            self.entity.direction = 'right'
            self.entity.ChangeAnimation('right')
        elif pressedKeys[pygame.K_DOWN]:
            self.entity.direction = 'down'
            self.entity.ChangeAnimation('down')
        elif pressedKeys[pygame.K_UP]:
            self.entity.direction = 'up'
            self.entity.ChangeAnimation('up')
        else:
            self.entity.ChangeState('idle')

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.entity.ChangeState('swing_sword')
                # if event.key == pygame.K_LEFT:
        #             self.entity.direction = 'left'
        #             self.entity.ChangeAnimation('walk_left')
        #         elif event.key == pygame.K_RIGHT:
        #             self.entity.direction = 'right'
        #             self.entity.ChangeAnimation('walk_right')
        #         elif event.key == pygame.K_UP:
        #             self.entity.direction = 'up'
        #             self.entity.ChangeAnimation('walk_up')
        #         elif event.key == pygame.K_DOWN:
        #             self.entity.direction = 'down'
        #             self.entity.ChangeAnimation('walk_down')

        #move and bump to the wall check
        super().update(dt, events)


        if self.bumped:
            if self.entity.direction == 'left':
                #temporal move to the wall (bumping effect)
                self.entity.x = self.entity.x - PLAYER_WALK_SPEED * dt

                for doorway in self.dungeon.current_room.doorways:
                    if self.entity.Collides(doorway) and doorway.open:
                        self.entity.y = doorway.y + 12
                        self.dungeon.BeginShifting(-WIDTH, 0)

                self.entity.x = self.entity.x + PLAYER_WALK_SPEED * dt

            elif self.entity.direction == 'right':
                self.entity.x = self.entity.x + PLAYER_WALK_SPEED * dt

                for doorway in self.dungeon.current_room.doorways:
                    if self.entity.Collides(doorway) and doorway.open:
                        self.entity.y = doorway.y + 12
                        self.dungeon.BeginShifting(WIDTH, 0)

                self.entity.x = self.entity.x - PLAYER_WALK_SPEED * dt

            elif self.entity.direction == 'up':
                self.entity.y = self.entity.y - PLAYER_WALK_SPEED * dt

                for doorway in self.dungeon.current_room.doorways:
                    if self.entity.Collides(doorway) and doorway.open:
                        self.entity.y = doorway.x + 24
                        self.dungeon.BeginShifting(0,  -HEIGHT)

                self.entity.y = self.entity.y + PLAYER_WALK_SPEED * dt

            else:
                self.entity.y = self.entity.y + PLAYER_WALK_SPEED * dt

                for doorway in self.dungeon.current_room.doorways:
                    if self.entity.Collides(doorway) and doorway.open:
                        self.entity.y = doorway.x + 24
                        self.dungeon.BeginShifting(0,  HEIGHT)

                self.entity.y = self.entity.y - PLAYER_WALK_SPEED * dt