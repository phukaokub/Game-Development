import pygame, sys

WIDTH = 1290
HEIGHT = 720

pygame.init()
font = pygame.font.SysFont('Helvetica', 24)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Custom event
timer_event1 = pygame.USEREVENT + 1
timer_event2 = pygame.USEREVENT + 2

pygame.time.set_timer(timer_event1, 1000)   # timer_event1 will be called every 1000 ms
pygame.time.set_timer(timer_event2, 1000)

class GameMain:
    def __init__(self):
        self.max_frame_rate = 60
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.timer1 = 0
        self.timer2 = 0

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == timer_event1:
                self.timer1 += 1
            elif event.type == timer_event2:
                self.timer2 += 1
        
    def render(self):
        self.screen.fill(BLACK)

        t_time = font.render(f'timer1: {str(self.timer1)}', False, WHITE)
        rect = t_time.get_rect(center=(WIDTH/2, HEIGHT/3))
        self.screen.blit(t_time, rect)

        t_time = font.render(f'timer2: {str(self.timer2)}', False, WHITE)
        rect = t_time.get_rect(center=(WIDTH/2, HEIGHT/3 + 100))
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