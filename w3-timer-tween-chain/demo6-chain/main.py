import pygame, sys
import tween
import random

WIDTH = 1290
HEIGHT = 720

pygame.init()
font = pygame.font.SysFont('Helvetica', 24)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

MOVE_DURATION = 3

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
        
        self.timer = 0
        self.flappy_x, self.flappy_y = 0, 0

        self.bird = Bird(self.flappy_x, self.flappy_y, 255)

        def first_move():
            tween.to(self.bird, 'x', WIDTH - self.image.get_width(), 
                     MOVE_DURATION).on_complete(second_move)
        def second_move():
            tween.to(self.bird, 'y', HEIGHT - self.image.get_height(), 
                     MOVE_DURATION).on_complete(third_move)
        def third_move():
            tween.to(self.bird, 'x', 0, 
                     MOVE_DURATION).on_complete(fourth_move)
        def fourth_move():
            tween.to(self.bird, 'y', 0, 
                     MOVE_DURATION).on_complete(first_move)
            
        first_move()

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tween.update(dt)
        
    def render(self):
        self.screen.fill(BLACK)
        self.bird.render(self.screen)

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