import pygame, sys

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


        self.second_counter = 0     # for counting second
        self.timer = 0              # for counting dt

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.timer += dt
        if self.timer > 1:  # 1 sec has passed
            self.second_counter += 1
            self.timer = self.timer % 1
        
    def render(self):
        self.screen.fill(BLACK)
        t_time = font.render(f'timer: {str(self.second_counter)}', False, WHITE)
        rect = t_time.get_rect(center=(WIDTH/2, HEIGHT/3))
        self.screen.blit(t_time, rect)

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