from src.states.BaseState import BaseState
from src.constants import *
from src.Dependency import *
import pygame, sys

from src.Paddle import Paddle
from src.LevelMaker import LevelMaker



class PaddleSelectState(BaseState):
    def __init__(self):
        super(PaddleSelectState, self).__init__()
        self.curr_paddle = 1

        self.l_arrow_image = sprite_collection["l_arrow"].image
        self.r_arrow_image = sprite_collection["r_arrow"].image

    def Exit(self):
        pass

    def Enter(self, params):
        self.high_scores = params['high_scores']

    def update(self,  dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.curr_paddle == 1:
                        gSounds['no-select'].play()
                    else:
                        gSounds['select'].play()
                        self.curr_paddle -= 1
                elif event.key == pygame.K_RIGHT:
                    if self.curr_paddle == 4:
                        gSounds['no-select'].play()
                    else:
                        self.curr_paddle += 1
                        gSounds['select'].play()

                if event.key == pygame.K_ESCAPE:
                    gSounds['wall-hit'].play()
                    g_state_manager.Change('start', {
                        'high_scores': self.high_scores
                    })

                if event.key == pygame.K_RETURN:
                    gSounds['confirm'].play()

                    g_state_manager.Change('serve', {
                        'level': 1,
                        'paddle': Paddle(self.curr_paddle),
                        'bricks': LevelMaker.CreateMap(1),
                        'health': 3,
                        'score': 0,
                        'high_scores': self.high_scores,
                        'recover_points': 5000
                    })

    def render(self, screen):
        t_instruct = gFonts['medium'].render("Select your paddle (left right)", False, (255, 255, 255))
        rect = t_instruct.get_rect(center=(WIDTH / 2, HEIGHT / 4))
        screen.blit(t_instruct, rect)

        t_enter = gFonts['small'].render("Press Enter to Play", False, (255, 255, 255))
        rect = t_enter.get_rect(center=(WIDTH / 2, HEIGHT / 3))
        screen.blit(t_enter, rect)


        if self.curr_paddle == 1:
            self.l_arrow_image.set_alpha(128)

        #rect = self.l_arrow_image.get_rect(center=(WIDTH/4 - 72, HEIGHT - HEIGHT/3))
        screen.blit(self.l_arrow_image, (WIDTH/4-72, HEIGHT - HEIGHT/3))
        self.l_arrow_image.set_alpha(255)

        if self.curr_paddle == 4:
            self.r_arrow_image.set_alpha(128)

        #rect = self.r_arrow_image.get_rect(center=(WIDTH - WIDTH/4, HEIGHT - HEIGHT/3))
        screen.blit(self.r_arrow_image, (WIDTH - WIDTH/4, HEIGHT - HEIGHT/3))
        self.r_arrow_image.set_alpha(255)

        paddle_img = paddle_image_list[self.curr_paddle-1]
        rect = paddle_img.get_rect(midtop=(WIDTH/2-96, HEIGHT - HEIGHT / 3))
        screen.blit(paddle_img, (WIDTH/2-96, HEIGHT - HEIGHT / 3))