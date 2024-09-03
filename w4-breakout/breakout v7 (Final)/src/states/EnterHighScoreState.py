from src.states.BaseState import BaseState
from src.constants import *
from src.resources import *
from src.Dependency import *
import pygame, sys

class EnterHighScoreState(BaseState):
    def __init__(self):
        super(EnterHighScoreState, self).__init__()
        self.chars = {
            '1':65,
            '2':65,
            '3':65,
        }

        self.highlighted_char = 1

    def Exit(self):
        pass

    def Enter(self, params):
        self.high_scores = params['high_scores']
        self.score = params['score']
        self.score_index = params['score_index']

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pass
                if event.key == pygame.K_LEFT and self.highlighted_char > 1:
                    self.highlighted_char -=1
                    gSounds['select'].play()
                elif event.key == pygame.K_RIGHT and self.highlighted_char < 3:
                    self.highlighted_char +=1
                    gSounds['select'].play()

                if event.key == pygame.K_UP:
                    self.chars[str(self.highlighted_char)] = self.chars[str(self.highlighted_char)] + 1
                    if self.chars[str(self.highlighted_char)] > 90:
                        self.chars[str(self.highlighted_char)] = 65
                elif event.key == pygame.K_DOWN:
                    self.chars[str(self.highlighted_char)] = self.chars[str(self.highlighted_char)] - 1
                    if self.chars[str(self.highlighted_char)] < 65:
                        self.chars[str(self.highlighted_char)] = 90

                if event.key == pygame.K_RETURN:
                    name = chr(self.chars['1'])+chr(self.chars['2']) + chr(self.chars['3'])

                    for i in range(8, self.score_index-1, -1):
                        #print(self.high_scores)
                        self.high_scores[i+1]['name'] = self.high_scores[i]['name']
                        self.high_scores[i + 1]['score'] = self.high_scores[i]['score']

                    self.high_scores[self.score_index]['name'] = name
                    self.high_scores[self.score_index]['score'] = self.score


                    with open(RANK_FILE_NAME, "w") as fp:
                        for i in range(10):
                            scores = self.high_scores[i]['name'] + '\n' + \
                                     str(self.high_scores[i]['score']) + '\n'
                            fp.write(scores)
                        fp.close()

                    g_state_manager.Change('high-scores', {
                        'high_scores': self.high_scores
                    })

    def render(self, screen):
        t_score = gFonts['medium'].render("Your score: " + str(self.score), False, (255, 255, 255))
        rect = t_score.get_rect(center=(WIDTH / 2, 90))
        screen.blit(t_score, rect)

        char1_color = (255, 255, 255)
        char2_color = (255, 255, 255)
        char3_color = (255, 255, 255)
        if self.highlighted_char == 1:
            char1_color = (103, 255, 255)
        elif self.highlighted_char == 2:
            char2_color = (103, 255, 255)
        elif self.highlighted_char == 3:
            char3_color = (103, 255, 255)

        t_char1 = gFonts['large'].render(chr(self.chars['1']), False, char1_color)
        t_char2 = gFonts['large'].render(chr(self.chars['2']), False, char2_color)
        t_char3 = gFonts['large'].render(chr(self.chars['3']), False, char3_color)

        rect = t_char1.get_rect(center=(WIDTH/2-84, HEIGHT/2))
        screen.blit(t_char1, rect)
        rect = t_char2.get_rect(center=(WIDTH / 2 - 18, HEIGHT / 2))
        screen.blit(t_char2, rect)
        rect = t_char3.get_rect(center=(WIDTH / 2 + 60, HEIGHT / 2))
        screen.blit(t_char3, rect)

