import pygame, sys

WIDTH = 1290
HEIGHT = 720

pygame.init()
font = pygame.font.SysFont('Helvetica', 24)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

MOVE_DURATION = 4

class GameMain:
    def __init__(self):
        self.max_frame_rate = 60
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.timer = 0
        self.image = pygame.image.load('../image/flappy.png') 
        self.flappy_x, self.flappy_y = 0, HEIGHT/2 - 24
        self.begin_x = self.flappy_x
        self.end_x = WIDTH - self.image.get_width()

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        if self.timer < MOVE_DURATION:
            self.timer += dt
            self.flappy_x = self.begin_x + (self.end_x - self.begin_x) * (self.timer / MOVE_DURATION)
        
    def render(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.image, (self.flappy_x, self.flappy_y))

    def PlayGame(self):
        clock = pygame.time.Clock()

        while True:
            dt = clock.tick(self.max_frame_rate) / 1000.0
            events = pygame.event.get()
            self.update(dt, events)
            self.render()
            pygame.display.update()

if __name__ == '__main__':
    main = GameMain()
    main.PlayGame()