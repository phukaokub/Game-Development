import pygame, sys
import tween
import random

WIDTH = 1290
HEIGHT = 720

pygame.init()
font = pygame.font.SysFont('Helvetica', 24)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

TIMER_MAX = 10
BIRDS_COUNT = 1000

class Bird:
    def __init__(self, x, y, opacity):
        self.image = pygame.image.load('../image/flappy.png').convert()
        self.x = x
        self.y = y
        self.opacity = opacity

    def render(self, screen):
        self.image.set_alpha(self.opacity)
        screen.blit(self.image, (self.x, self.y)) 

class GameMain:
    def __init__(self):
        self.max_frame_rate = 60
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.image = pygame.image.load('../image/flappy.png')
        self.birds = []
        self.end_x = WIDTH - self.image.get_width()
        self.end_opacity = 255

        for i in range(BIRDS_COUNT):
            random_y = random.random() * (HEIGHT - self.image.get_height())
            bird = Bird(0, random_y, 0)
            self.birds.append(bird)

            tween_time = random.random() * TIMER_MAX
            tween.to(self.birds[i], 'x', self.end_x, tween_time)
            tween.to(self.birds[i], 'opacity', self.end_opacity, tween_time)

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tween.update(dt)
        
    def render(self):
        self.screen.fill(BLACK)
        for i in range(BIRDS_COUNT):
            self.birds[i].render(self.screen)

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