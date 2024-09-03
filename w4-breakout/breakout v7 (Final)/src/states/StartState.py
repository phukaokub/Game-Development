from src.states.BaseState import BaseState
import pygame, sys
from src.constants import *
from src.Dependency import *

class StartState(BaseState):
    def __init__(self):
        super(StartState, self).__init__()
        #start = 1,       ranking = 2
        self.option = 1

    def Exit(self):
        pass

    def Enter(self, params):
        self.high_scores = params['high_scores']

    def render(self, screen):
        # title
        t_title = gFonts['large'].render("BREAKOUT", False, (255, 255, 255))
        rect = t_title.get_rect(center=(WIDTH / 2, HEIGHT / 3))
        screen.blit(t_title, rect)

        t_start_color = (255, 255, 255)
        t_highscore_color = (255, 255, 255)

        if self.option == 1:
            t_start_color = (103, 255, 255)

        if self.option == 2:
            t_highscore_color = (103, 255, 255)

        t_start = gFonts['medium'].render("START", False, t_start_color)
        rect = t_start.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 210))
        screen.blit(t_start, rect)
        t_highscore = gFonts['medium'].render("HIGH SCORES", False, t_highscore_color)
        rect = t_highscore.get_rect(center=(WIDTH/2, HEIGHT/2 + 280))
        screen.blit(t_highscore, rect)

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    if self.option==1:
                        self.option=2
                    else:
                        self.option=1
                    gSounds['paddle-hit'].play()

                if event.key == pygame.K_RETURN:
                    gSounds['confirm'].play()

                    if self.option == 1:
                        g_state_manager.Change('paddle-select', {
                            'high_scores': self.high_scores
                        })
                    else:
                        g_state_manager.Change('high-scores', {
                            'high_scores': self.high_scores
                        })
