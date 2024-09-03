import pygame, math
from pygame import mixer
from src.constants import *


pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()

music_channel = mixer.Channel(0)
music_channel.set_volume(0.2)

from src.Dependency import *

# Credit for graphics:
# https://opengameart.org/users/buch
#
# Credit for music:
# http://freesound.org/people/joshuaempyre/sounds/251461/
# http://www.soundcloud.com/empyreanma


class GameMain:
    def __init__(self):
        self.max_frame_rate = 60
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.bg_image = pygame.image.load("./graphics/background.png")

        self.bg_image = pygame.transform.scale(
            self.bg_image, (WIDTH+5, HEIGHT+5))

        self.bg_music = pygame.mixer.Sound('sounds/music.wav')

        g_state_manager.SetScreen(self.screen)

        states = {
            'start': StartState(),
            'play': PlayState(),
            'serve': ServeState(),
            'game-over': GameOverState(),
            'victory': VictoryState(),
        }
        g_state_manager.SetStates(states)


    def RenderBackground(self):
        main.screen.blit(self.bg_image, (0, 0))

    def PlayGame(self):
        self.bg_music.play(-1)
        clock = pygame.time.Clock()
        g_state_manager.Change('start', {

        })

        while True:
            pygame.display.set_caption("breakout game running with {:d} FPS".format(int(clock.get_fps())))
            dt = clock.tick(self.max_frame_rate) / 1000.0

            #input
            events = pygame.event.get()

            #update
            g_state_manager.update(dt, events)

            #bg render
            self.RenderBackground()
            #render
            g_state_manager.render()

            #screen update
            pygame.display.update()


if __name__ == '__main__':
    main = GameMain()

    main.PlayGame()



