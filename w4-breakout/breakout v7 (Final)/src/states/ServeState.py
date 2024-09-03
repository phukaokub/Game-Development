import random, pygame, sys
from src.states.BaseState import BaseState
from src.constants import *
from src.resources import *
from src.Dependency import *


import src.CommonRender as CommonRender
from src.Ball import Ball

class ServeState(BaseState):
    def __init__(self):
        super(ServeState, self).__init__()

    def Enter(self, params):
        self.paddle = params["paddle"]
        self.bricks = params["bricks"]
        self.health = params["health"]
        self.score = params["score"]
        self.high_scores = params["high_scores"]
        self.level = params["level"]
        self.recover_points = params["recover_points"]

        self.ball = Ball(1)
        self.ball.skin = random.randint(0, 6)

    def Exit(self):
        pass

    def update(self,  dt, events):
        self.paddle.update(dt)
        # put the ball above the paddle
        self.ball.rect.x = self.paddle.x + (self.paddle.width/2) - 12
        self.ball.rect.y = self.paddle.y - 24

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    g_state_manager.Change('play', {
                        'paddle':self.paddle,
                        'level':self.level,
                        'health':self.health,
                        'score':self.score,
                        'high_scores': self.high_scores,
                        'ball':self.ball,
                        'recover_points': self.recover_points,
                        'bricks':self.bricks
                    })

    def render(self, screen):
        self.paddle.render(screen)
        self.ball.render(screen)

        for brick in self.bricks:
            brick.render(screen)

        CommonRender.RenderScore(screen, self.score)
        CommonRender.RenderHealth(screen, self.health)

        t_level = gFonts['large'].render("Level" + str(self.level), False, (255, 255, 255))
        rect = t_level.get_rect(center=(WIDTH/2, HEIGHT / 3))
        screen.blit(t_level, rect)

        t_press_enter = gFonts['medium'].render("Press Enter to Serve", False, (255, 255, 255))
        rect = t_press_enter.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(t_press_enter, rect)