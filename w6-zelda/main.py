import pygame
import sys
import Util

WIDTH = 1280
HEIGHT = 720

TILE_SIZE = 32
CHARACTER_WIDTH = 16
CHARACTER_HEIGHT = 16

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()

SKY = 35
GRASS = 33
GROUND_BOUNDARY = 43
GROUND = 53

CHARACTER_CAMERA_SPEED = 120
CAMERA_SCROLL_SPEED = 120

class GameMain:
    def __init__(self):
        self.max_frame_rate = 60
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.tilemaps = Util.GenerateTiles('tiles.png', TILE_SIZE, TILE_SIZE,
                                           colorkey=-1, scale=3)
        
        self.sprite_collection = Util.SpriteManager().spriteCollection
        self.animation = self.sprite_collection['character_front'].animation

        self.character_x = WIDTH/2 - (CHARACTER_WIDTH/2)
        self.character_y = (5*TILE_SIZE - CHARACTER_HEIGHT) * 3
        self.direction = 'front' #left right front
        
        self.map_width = WIDTH // (TILE_SIZE * 3) + 1
        self.map_height = HEIGHT // (TILE_SIZE * 3) + 1

        self.camera_x_scroll = 0
        self.camera_y_scroll = 0

        self.tiles = []

        for y in range(self.map_height):
            self.tiles.append([])
            for x in range(self.map_width):
                if y <4:
                    self.tiles[y].append(SKY)
                elif y == 4:
                    self.tiles[y].append(GRASS)
                elif y == 5:
                    self.tiles[y].append(GROUND_BOUNDARY)
                else:
                    self.tiles[y].append(GROUND)

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pressedKeys = pygame.key.get_pressed()
        if pressedKeys[pygame.K_LEFT]:
            self.direction = 'left'
            self.animation = self.sprite_collection['character_walk_right'].animation
            # self.camera_x_scroll -= CAMERA_SCROLL_SPEED * dt
        elif pressedKeys[pygame.K_RIGHT]:
            self.direction = 'right'
            self.animation = self.sprite_collection['character_walk_right'].animation
            # self.camera_x_scroll += CAMERA_SCROLL_SPEED * dt
        else:
            self.direction = 'front'
            self.animation = self.sprite_collection['character_front'].animation
            # self.camera_y_scroll -= CAMERA_SCROLL_SPEED * dt

        if self.direction == 'left':
            self.character_x -= CHARACTER_CAMERA_SPEED * dt
        elif self.direction == 'right':
            self.character_x += CHARACTER_CAMERA_SPEED * dt

        self.camera_x_scroll = self.character_x - WIDTH/2 + (CHARACTER_WIDTH/2)

    def render(self):
        self.screen.fill((0, 0, 200))

        for y in range(self.map_height):
            for x in range(self.map_width):
                id = self.tiles[y][x]
                self.screen.blit(self.tilemaps[id], 
                                 (-self.camera_x_scroll + x*TILE_SIZE * 3, 
                                  -self.camera_y_scroll + y*TILE_SIZE * 3))
        
        char_img = self.animation.image
        if self.direction == 'left':
            char_img = pygame.transform.flip(char_img, True, False)

        self.screen.blit(   char_img, (self.character_x, self.character_y))

    def PlayGame(self):
        clock = pygame.time.Clock()

        while True:
            pygame.display.set_caption(
                "running with {:d} FPS".format(int(clock.get_fps())))
            dt = clock.tick(self.max_frame_rate) / 1000.0

            # input
            events = pygame.event.get()

            # update
            self.update(dt, events)

            # render
            self.render()

            # screen update
            pygame.display.update()


if __name__ == '__main__':
    main = GameMain()

    main.PlayGame()
