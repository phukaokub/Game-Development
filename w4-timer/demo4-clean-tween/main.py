import pygame, sys
import os

WIDTH = 1290
HEIGHT = 720

pygame.init()
font = pygame.font.SysFont('Helvetica', 24)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class GameMain:
    def __init__(self):
        self.max_frame_rate = 60
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        base_path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_path, '../image/floppy_bird.png')
        self.image = pygame.image.load(image_path)


    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
    def render(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.image, (WIDTH/2 - self.image.get_width()/2, HEIGHT/2 - self.image.get_height()/2))
        

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