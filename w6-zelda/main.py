import pygame, sys, Util

WIDTH = 1280
HEIGHT = 720

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()

class GameMain:
    def __init__(self):
        self.max_frame_rate = 60
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def render(self):
        self.screen.fill((0, 0, 200))

    def PlayGame(self):
        clock = pygame.time.Clock()

        while True:
            pygame.display.set_caption("running with {:d} FPS".format(int(clock.get_fps())))
            dt = clock.tick(self.max_frame_rate) / 1000.0

            #input
            events = pygame.event.get()

            #update
            self.update(dt, events)

            #render
            self.render()

            #screen update
            pygame.display.update()


if __name__ == '__main__':
    main = GameMain()

    main.PlayGame()



