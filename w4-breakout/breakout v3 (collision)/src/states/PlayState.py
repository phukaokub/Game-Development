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
            ####can be fixed to make it natural####
            self.ball.rect.y = self.paddle.rect.y - 24
            self.ball.dy = -self.ball.dy

            # half left hit while moving left (side attack) the more side, the faster
            if self.ball.rect.x + self.ball.rect.width < self.paddle.rect.x + (self.paddle.width / 2) and self.paddle.dx < 0:
                self.ball.dx = -150 + -(8 * (self.paddle.rect.x + self.paddle.width / 2 - self.ball.rect.x))
            # right paddle and moving right (side attack)
            elif self.ball.rect.x > self.paddle.rect.x + (self.paddle.width / 2) and self.paddle.dx > 0:
                self.ball.dx = 150 + (8 * abs(self.paddle.rect.x + self.paddle.width / 2 - self.ball.rect.x))
            gSounds['paddle-hit'].play()

        for k, brick in enumerate(self.bricks):
            if brick.alive and self.ball.Collides(brick):
                brick.Hit()

                # hit brick from left while moving right -> x flip
                if self.ball.rect.x + 6 < brick.rect.x and self.ball.dx > 0:
                    self.ball.dx = -self.ball.dx
                    self.ball.rect.x = brick.rect.x - 24

                # hit brick from right while moving left -> x flip
                elif self.ball.rect.x + 18 > brick.rect.x + brick.width and self.ball.dx < 0:
                    self.ball.dx = -self.ball.dx
                    self.ball.rect.x = brick.rect.x + 96

                # hit from above -> y flip
                elif self.ball.rect.y < brick.rect.y:
                    self.ball.dy = -self.ball.dy
                    self.ball.rect.y = brick.rect.y - 24

                # hit from bottom -> y flip
                else:
                    self.ball.dy = -self.ball.dy
                    self.ball.rect.y = brick.rect.y + 48

                # whenever hit, speed is slightly increase, maximum is 450
                if abs(self.ball.dy) < 450:
                    self.ball.dy = self.ball.dy * 1.02

                break

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

