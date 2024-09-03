from src.states.BaseState import BaseState
from src.constants import *
from src.Dependency import *
import pygame, sys

class GameOverState(BaseState):
    def __init__(self):
        super(GameOverState, self).__init__()

    def Exit(self):
        pass

    def Enter(self, params):
        self.score = params['score']

    def update(self,  dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    g_state_manager.Change('start', {
                    })

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def render(self, screen):
        t_gameover = gFonts['large'].render("GAME OVER", False, (255, 255, 255))
        rect = t_gameover.get_rect(center=(WIDTH / 2, HEIGHT/3))
        screen.blit(t_gameover, rect)

        t_score = gFonts['medium'].render("Final Score: " + str(self.score), False, (255, 255, 255))
        rect = t_score.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(t_score, rect)

        t_instruct = gFonts['medium'].render("Press Enter to Play Again", False, (255, 255, 255))
        rect = t_instruct.get_rect(center=(WIDTH / 2, HEIGHT - HEIGHT / 4))
        screen.blit(t_instruct, rect)