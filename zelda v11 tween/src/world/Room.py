import random

from src.entity_defs import *
from src.constants import *
from src.Dependencies import *
from src.world.Doorway import Doorway
from src.EntityBase import EntityBase
from src.entity_defs import EntityConf
from src.states.entity.EntityIdleState import EntityIdleState
from src.states.entity.EntityWalkState import EntityWalkState
from src.states.entity.SlimeAttackState import SlimeAttackState
from src.StateMachine import StateMachine
from src.GameObject import GameObject
from src.object_defs import *
import pygame


class Room:
    def __init__(self, player):
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT

        # for collisions
        self.player = player

        self.tiles = []
        self.GenerateWallsAndFloors()

        self.entities = []
        self.GenerateEntities()

        self.objects = []
        self.GenerateObjects()

        self.doorways = []
        self.doorways.append(Doorway('top', False, self))
        self.doorways.append(Doorway('botoom', False, self))
        self.doorways.append(Doorway('left', False, self))
        self.doorways.append(Doorway('right', False, self))

        # centering the dungeon rendering
        self.render_offset_x = MAP_RENDER_OFFSET_X
        self.render_offset_y = MAP_RENDER_OFFSET_Y

        self.render_entity = True

        self.adjacent_offset_x = 0
        self.adjacent_offset_y = 0

    def GenerateWallsAndFloors(self):
        for y in range(1, self.height+1):
            self.tiles.append([])
            for x in range(1, self.width+1):
                id = TILE_EMPTY

                # Wall Corner
                if x == 1 and y == 1:
                    id = TILE_TOP_LEFT_CORNER
                elif x == 1 and y == self.height:
                    id = TILE_BOTTOM_LEFT_CORNER
                elif x == self.width and y == 1:
                    id = TILE_TOP_RIGHT_CORNER
                elif x == 1 and y == self.height:
                    id = TILE_BOTTOM_RIGHT_CORNER

                # Wall, Floor
                elif x == 1:
                    id = random.choice(TILE_LEFT_WALLS)
                elif x == self.width:
                    id = random.choice(TILE_RIGHT_WALLS)
                elif y == 1:
                    id = random.choice(TILE_TOP_WALLS)
                elif y == self.height:
                    id = random.choice(TILE_BOTTOM_WALLS)
                else:
                    id = random.choice(TILE_FLOORS)

                self.tiles[y-1].append(id)

    def GenerateEntities(self):
        types = ['skeleton']

        for i in range(random.randrange(self.player.difficulty + 2, self.player.difficulty*2 + 2)):
            type = random.choice(types)

            conf = EntityConf(type=ENTITY_DEFS[type].type,
                              animation=ENTITY_DEFS[type].animation,
                              walk_speed=ENTITY_DEFS[type].walk_speed,
                              health=ENTITY_DEFS[type].health +
                              self.player.difficulty,
                              x=random.randrange(
                                  MAP_RENDER_OFFSET_X+TILE_SIZE, WIDTH - TILE_SIZE * 2 - 48),
                              y=random.randrange(MAP_RENDER_OFFSET_Y+TILE_SIZE, HEIGHT-(
                                  HEIGHT-MAP_HEIGHT*TILE_SIZE)+MAP_RENDER_OFFSET_Y - TILE_SIZE - 48),
                              width=ENTITY_DEFS[type].width, height=ENTITY_DEFS[type].height)

            self.entities.append(EntityBase(conf))

            self.entities[i].state_machine = StateMachine()
            self.entities[i].state_machine.SetScreen(
                pygame.display.get_surface())
            self.entities[i].state_machine.SetStates({
                "walk": EntityWalkState(self.entities[i]),
                "idle": EntityIdleState(self.entities[i])
            })

            self.entities[i].ChangeState("walk")

        # Add slime boss
        if self.player.difficulty >= 5:
            type = 'slime'
            for j in range(random.randint(1, math.floor(self.player.difficulty / 3) + 1)):
                conf = EntityConf(type=ENTITY_DEFS[type].type,
                                  animation=ENTITY_DEFS[type].animation,
                                  walk_speed=ENTITY_DEFS[type].walk_speed,
                                  health=ENTITY_DEFS[type].health +
                                  math.floor(self.player.difficulty/2),
                                  x=random.randrange(
                    MAP_RENDER_OFFSET_X+TILE_SIZE, WIDTH - TILE_SIZE * 2 - 48),
                    y=random.randrange(MAP_RENDER_OFFSET_Y+TILE_SIZE, HEIGHT-(
                        HEIGHT-MAP_HEIGHT*TILE_SIZE)+MAP_RENDER_OFFSET_Y - TILE_SIZE - 48),
                    width=ENTITY_DEFS[type].width, height=ENTITY_DEFS[type].height)

                slime_entity = EntityBase(conf)

                slime_entity.state_machine = StateMachine()
                slime_entity.state_machine.SetScreen(
                    pygame.display.get_surface())
                slime_entity.state_machine.SetStates({
                    "walk": EntityWalkState(slime_entity),
                    "idle": EntityIdleState(slime_entity),
                    'attack': SlimeAttackState(slime_entity)
                })

                slime_entity.ChangeState("walk")
                self.entities.append(slime_entity)

    def GenerateObjects(self):
        switch = GameObject(GAME_OBJECT_DEFS['switch'],
                            x=random.randint(
                                MAP_RENDER_OFFSET_X + TILE_SIZE, WIDTH-TILE_SIZE*2 - 48),
                            y=random.randint(MAP_RENDER_OFFSET_Y+TILE_SIZE, HEIGHT-(HEIGHT-MAP_HEIGHT*TILE_SIZE) + MAP_RENDER_OFFSET_Y - TILE_SIZE - 48))

        def switch_function():
            if switch.state == "unpressed":
                switch.state = "pressed"

                for doorway in self.doorways:
                    doorway.open = True
                gSounds['door'].play()

        switch.on_collide = switch_function

        self.objects.append(switch)

        for i in range(random.randint(1, 3)):
            while True:
                x = random.randint(MAP_RENDER_OFFSET_X +
                                   TILE_SIZE, WIDTH - TILE_SIZE * 2 - 16)
                y = random.randint(MAP_RENDER_OFFSET_Y + TILE_SIZE, HEIGHT - (
                    HEIGHT - MAP_HEIGHT * TILE_SIZE) + MAP_RENDER_OFFSET_Y - TILE_SIZE - 16)
                if not any(obj.x == x and obj.y == y for obj in self.objects):
                    break

            pot = GameObject(GAME_OBJECT_DEFS['pot'], x=x, y=y)
            self.objects.append(pot)

    def update(self, dt, events):
        if self.adjacent_offset_x != 0 or self.adjacent_offset_y != 0:
            return

        self.player.update(dt, events)

        for entity in self.entities:
            if entity.health <= 0:
                entity.is_dead = True
                self.player.level += 0.25
                self.entities.remove(entity)
            elif not entity.is_dead:
                entity.ProcessAI({"room": self}, dt)
                entity.update(dt, events)

            if not entity.is_dead and self.player.Collides(entity) and not self.player.invulnerable:
                gSounds['hit_player'].play()
                self.player.Damage(1)
                self.player.SetInvulnerable(1.5)

            if entity.type == 'slime':
                if entity.is_attacked:
                    for i in range (0,4):
                        if i == 0:
                            direction = 'left'
                        elif i == 1:
                            direction = 'right'
                        elif i == 2:
                            direction = 'up'
                        elif i == 3:
                            direction = 'down'
                        object = GameObject(GAME_OBJECT_DEFS['bucket'], x=entity.x, y=entity.y, direction=direction)
                        self.objects.append(object)
                        if len(entity.carrying_object) == 4:
                            entity.carrying_object = []
                        entity.carrying_object.append(object)
                        entity.carrying_object[i].throw(direction, 5)
                        entity.is_attacked = False
                        
        for obj in self.objects:
            obj.update(dt)
            # Count the number of 'bucket' type objects
            bucket_count = sum(1 for obj in self.objects if obj.type == 'bucket')
            if self.player.Collides(obj):
                if obj.type == "switch":
                    obj.on_collide()
                if obj.type == "heal":
                    gSounds['heal'].play()
                    self.player.health += 1
                    self.objects.remove(obj)
                if obj.type == "atkUp":
                    gSounds['atkUp'].play()
                    self.player.atkUp += 0.5
                    self.objects.remove(obj)
                if obj.type == "increase_level":
                    gSounds['increase_level'].play()
                    self.player.level += 1
                    self.objects.remove(obj)

            # Check pot collision for entities and spawn power-up on destruction
            if obj.type == "pot" and obj.state == "thrown":
                for entity in self.entities:
                    if entity.Collides(obj) and not entity.is_dead:
                        gSounds['hit_enemy'].play()
                        entity.Damage(10)
                        obj.velocity_x = 0
                        obj.velocity_y = 0
                        obj.state = "destroyed"
                        obj.is_thrown = False

                if abs(obj.x - obj.start_x) > 300 or abs(obj.y - obj.start_y) > 300:
                    obj.is_thrown = False
                    self.spawn_powerup(obj.powerup)
                    self.objects.remove(obj)
                    obj.start_x = None
                    obj.start_y = None
                elif obj.y > TILE_SIZE * MAP_HEIGHT or obj.y < MAP_RENDER_OFFSET_Y + TILE_SIZE or obj.x > TILE_SIZE * MAP_WIDTH - MAP_RENDER_OFFSET_X or obj.x < MAP_RENDER_OFFSET_X + TILE_SIZE:
                    obj.is_thrown = False
                    self.spawn_powerup(obj.powerup)
                    self.objects.remove(obj)
                    obj.start_x = None
                    obj.start_y = None
                
            if obj.type == "bucket" and obj.is_thrown:
                if self.player.Collides(obj):
                    self.objects.remove(obj)
                    gSounds['hit_player'].play()
                    self.player.Damage(3)
                    self.player.SetInvulnerable(1.5)
                if abs(obj.x - obj.start_x) > 300 or abs(obj.y - obj.start_y) > 300:
                    obj.is_thrown = False
                    obj.start_x = None
                    obj.start_y = None
                    self.objects.remove(obj)


    def render(self, screen, x_mod, y_mod, shifting):
        for y in range(self.height):
            for x in range(self.width):
                tile_id = self.tiles[y][x]
                # need to access tile_id - 1  <-- actual list is start from 0
                screen.blit(gRoom_image_list[tile_id-1], (x * TILE_SIZE + self.render_offset_x + self.adjacent_offset_x + x_mod,
                            y * TILE_SIZE + self.render_offset_y + self.adjacent_offset_y + y_mod))

        for doorway in self.doorways:
            doorway.render(screen, self.adjacent_offset_x +
                           x_mod, self.adjacent_offset_y+y_mod)

        for object in self.objects:
            object.render(self.player, screen, self.adjacent_offset_x +
                          x_mod, self.adjacent_offset_y+y_mod)

        if not shifting:
            for entity in self.entities:
                if not entity.is_dead:
                    entity.render(self.adjacent_offset_x,
                                  self.adjacent_offset_y + y_mod)
            if self.player:
                self.player.render()

        # render player level at top corner
        font = pygame.font.Font(None, 36)
        player_level = font.render(
            "Player Level: " + str(self.player.level), True, (255, 255, 255))
        screen.blit(player_level, (180, 15))

        # render player atkUp at top corner
        player_atkUp = font.render(
            "Player Attack: " + str(self.player.attack), True, (255, 255, 255))
        screen.blit(player_atkUp, (400, 15))

    def spawn_powerup(self, powerup):
        self.objects.append(powerup)
