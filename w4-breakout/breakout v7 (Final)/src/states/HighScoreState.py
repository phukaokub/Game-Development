from src.states.BaseState import BaseState
from src.constants import *
from src.resources import *
from src.Dependency import *

import pygame, sys

class HighScoreState(BaseState):
    def __init__(self):
        super(HighScoreState, self).__init__()

    def Exit(self):
        pass

    def Enter(self, params):
        self.high_scores = params['high_scores']

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gSounds['wall-hit'].play()
                    g_state_manager.Change('start', {
                        'high_scores': self.high_scores
                    })

    def render(self, screen):
        t_high_score = gFonts['large'].render("High Scores", False, (255, 255, 255))
        rect = t_high_score.get_rect(center=(WIDTH/2, 60))
        screen.blit(t_high_score, rect)

        for i in range(10):
            name = self.high_scores[i]['name']
            score = self.high_scores[i]['score']

            t_index = gFonts['medium'].render(str(i+1) + '.', False, (255, 255, 255))
            rect = t_index.get_rect(topright=(WIDTH/4 + 200, 180+i*39))
            screen.blit(t_index, rect)

            t_name = gFonts['medium'].render(name, False, (255, 255, 255))
            rect = t_name.get_rect(topright=(WIDTH/4 + 114 + 250, 180 + i * 39))
            screen.blit(t_name, rect)

            t_score = gFonts['medium'].render(str(score), False, (255, 255, 255))
            rect = t_score.get_rect(topright=(WIDTH / 2 + 200, 180 + i * 39))
            screen.blit(t_score, rect)

            t_escape_message = gFonts['small'].render("Press Escape to return to the main menu", False, (255, 255, 255))
            rect = t_escape_message.get_rect(center=(WIDTH/2, HEIGHT-54))
            screen.blit(t_escape_message, rect)