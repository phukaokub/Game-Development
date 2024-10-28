import random

from src.entity_defs import *
from src.constants import *
from src.Dependencies import *
from src.world.Doorway import Doorway
from src.EntityBase import EntityBase
from src.entity_defs import EntityConf
from src.states.entity.EntityIdleState import EntityIdleState
from src.states.entity.EntityWalkState import EntityWalkState
from src.StateMachine import StateMachine
from src.GameObject import GameObject
from src.object_defs import *
import pygame


class Room:
    def __init__(self, player):
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT

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

        # for collisions
        self.player = player

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

        for i in range(NUMBER_OF_MONSTER):
            type = random.choice(types)

            conf = EntityConf(animation=ENTITY_DEFS[type].animation,
                              walk_speed=ENTITY_DEFS[type].walk_speed,
                              x=random.randrange(
                                  MAP_RENDER_OFFSET_X+TILE_SIZE, WIDTH - TILE_SIZE * 2 - 48),
                              y=random.randrange(MAP_RENDER_OFFSET_Y+TILE_SIZE, HEIGHT-(
                                  HEIGHT-MAP_HEIGHT*TILE_SIZE)+MAP_RENDER_OFFSET_Y - TILE_SIZE - 48),
                              width=ENTITY_DEFS[type].width, height=ENTITY_DEFS[type].height, health=ENTITY_DEFS[type].health)

            self.entities.append(EntityBase(conf))

            self.entities[i].state_machine = StateMachine()
            self.entities[i].state_machine.SetScreen(
                pygame.display.get_surface())
            self.entities[i].state_machine.SetStates({
                "walk": EntityWalkState(self.entities[i]),
                "idle": EntityIdleState(self.entities[i])
            })

            self.entities[i].ChangeState("walk")

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

        for i in range(random.randint(3, 6)):
            while True:
                x = random.randint(MAP_RENDER_OFFSET_X + TILE_SIZE, WIDTH - TILE_SIZE * 2 - 16)
                y = random.randint(MAP_RENDER_OFFSET_Y + TILE_SIZE, HEIGHT - (HEIGHT - MAP_HEIGHT * TILE_SIZE) + MAP_RENDER_OFFSET_Y - TILE_SIZE - 16)
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
                self.entities.remove(entity)
            elif not entity.is_dead:
                entity.ProcessAI({"room": self}, dt)
                entity.update(dt, events)

            if not entity.is_dead and self.player.Collides(entity) and not self.player.invulnerable:
                gSounds['hit_player'].play()
                self.player.Damage(1)
                self.player.SetInvulnerable(1.5)

        for obj in self.objects:
            obj.update(dt)
            if self.player.Collides(obj):
                if obj.type == "switch":
                    obj.on_collide()
                if obj.type == "heal":
                    self.player.health += 1
                    self.objects.remove(obj)
                if obj.type == "atkUp":
                    self.player.attack += 1
                    self.objects.remove(obj)
                if obj.type == "increase_level":
                    self.player.level += 1
                    print("player level: ", self.player.level)
                    self.objects.remove(obj)

            # Check pot collision for entities and spawn power-up on destruction
            if obj.type == "pot" and obj.state == "thrown":
                for entity in self.entities:
                    if entity.Collides(obj) and not entity.is_dead:
                        gSounds['hit_enemy'].play()
                        entity.Damage(2)
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
        
        # render player level at top right corner
        font = pygame.font.Font(None, 36)
        text = font.render("Player Level: " + str(self.player.level), True, (255,255,255))
        screen.blit(text, (180, 15))


    def spawn_powerup(self, powerup):
        self.objects.append(powerup)
