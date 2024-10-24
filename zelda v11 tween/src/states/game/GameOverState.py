from src.states.BaseState import BaseState
import pygame, sys
from src.recourses import *
from src.constants import *

class GameOverState(BaseState):
    def __init__(self):
        pass

    def Exit(self):
        pass
    def Enter(self, params):
        pass

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    g_state_manager.Change('start')


    def render(self, screen):
        t_title = gFonts['zelda'].render("GAME OVER", False, (175, 53, 42))
        rect = t_title.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 144))
        screen.blit(t_title, rect)

        t_press_enter = gFonts['zelda_small'].render("Press Enter", False, (175, 53, 42))
        rect = t_press_enter.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 48))
        screen.blit(t_press_enter, rect)
