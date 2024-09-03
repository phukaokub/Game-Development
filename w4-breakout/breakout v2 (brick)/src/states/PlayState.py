import random, pygame, sys
from src.states.BaseState import BaseState
from src.constants import *
from src.Dependency import *

class PlayState(BaseState):
    def __init__(self):
        super(PlayState, self).__init__()
        self.paused = False
        self.paddle = Paddle()
        self.ball = Ball(1)

        self.ball.x = WIDTH / 2 - 12
        self.ball.y = HEIGHT - 126

        self.ball.dx = random.randint(-600, 600)  # -200 200
        self.ball.dy = random.randint(-180, -150)

        self.bricks= LevelMaker.CreateMap(1)

    def Enter(self, params):
        pass


    def update(self,  dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                    gSounds['pause'].play()
                    #music_channel.play(sounds_list['pause'])
        if self.paused:
            return

        self.paddle.update(dt)
        self.ball.update(dt)

        if self.ball.Collides(self.paddle):
            # raise ball above paddle
            self.ball.dy = -self.ball.dy

            gSounds['paddle-hit'].play()

        for k, brick in enumerate(self.bricks):
            if brick.alive and self.ball.Collides(brick):
                brick.Hit()

    def Exit(self):
        pass

    def render(self, screen):
        for brick in self.bricks:
            brick.render(screen)

        self.paddle.render(screen)
        self.ball.render(screen)

        if self.paused:
            t_pause = gFonts['large'].render("PAUSED", False, (255, 255, 255))
            rect = t_pause.get_rect(center = (WIDTH/2, HEIGHT/2))
            screen.blit(t_pause, rect)

