import random, pygame, sys
from src.states.BaseState import BaseState
from src.constants import *
from src.resources import *
from src.Dependency import *

import src.CommonRender as CommonRender
from src.Ball import Ball

class UpgradeState(BaseState):
    def init(self):
        super(UpgradeState, self).__init__()

    def Enter(self, params):
        self.paddle = params["paddle"]
        self.bricks = params["bricks"]
        self.health = params["health"]
        self.score = params["score"]
        self.high_scores = params["high_scores"]
        self.level = params["level"]
        self.recover_points = params["recover_points"]

        self.upgrade = Upgrade()
        self.ball = Ball(1)
        self.ball.skin = random.randint(0, 6)

        self.item1_cost = self.upgrade.calculate_upgrade_cost(self.paddle.item1_level, self.level)
        self.item2_cost = self.upgrade.calculate_upgrade_cost(self.paddle.item2_level, self.level)
        self.item3_cost = self.upgrade.calculate_upgrade_cost(self.paddle.item3_level, self.level)
        self.item4_cost = self.upgrade.calculate_upgrade_cost(self.paddle.item4_level, self.level)
    
    def Exit(self):
        pass

    def update(self,  dt, events):
        self.upgrade.update(dt, events)

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.upgrade.select == 1:
                        if self.paddle.upgrade_point >= self.item1_cost:
                            self.paddle.item1_level += 1
                            self.paddle.upgrade_point -= self.item1_cost
                            gSounds['select'].play()
                            g_state_manager.Change('serve', {
                                'paddle': self.paddle,
                                'level': self.level,  # Move to the next level
                                'bricks': self.bricks,  # Use the new map for the next level
                                'health': self.health,
                                'score': self.score,
                                'high_scores': self.high_scores,
                                'recover_points': self.recover_points,
                            })
                        else:
                            gSounds['no-select'].play()
                    elif self.upgrade.select == 2:
                        if self.paddle.upgrade_point >= self.item2_cost:
                            self.paddle.item2_level += 1
                            self.paddle.upgrade_point -= self.item2_cost
                            gSounds['select'].play()
                            g_state_manager.Change('serve', {
                                'paddle': self.paddle,
                                'level': self.level,  # Move to the next level
                                'bricks': self.bricks,  # Use the new map for the next level
                                'health': self.health,
                                'score': self.score,
                                'high_scores': self.high_scores,
                                'recover_points': self.recover_points,
                            })
                        else:
                            gSounds['no-select'].play()
                    elif self.upgrade.select == 3:
                        if self.paddle.upgrade_point >= self.item3_cost:
                            self.paddle.item3_level += 1
                            self.paddle.upgrade_point -= self.item3_cost
                            gSounds['select'].play()
                            g_state_manager.Change('serve', {
                                'paddle': self.paddle,
                                'level': self.level,  # Move to the next level
                                'bricks': self.bricks,  # Use the new map for the next level
                                'health': self.health,
                                'score': self.score,
                                'high_scores': self.high_scores,
                                'recover_points': self.recover_points,
                            })
                        else:
                            gSounds['no-select'].play()
                    elif self.upgrade.select == 4:
                        if self.paddle.upgrade_point >= self.item4_cost:
                            self.paddle.item4_level += 1
                            self.paddle.upgrade_point -= self.item4_cost
                            gSounds['select'].play()
                            g_state_manager.Change('serve', {
                                'paddle': self.paddle,
                                'level': self.level,  # Move to the next level
                                'bricks': self.bricks,  # Use the new map for the next level
                                'health': self.health,
                                'score': self.score,
                                'high_scores': self.high_scores,
                                'recover_points': self.recover_points,
                            })
                        else:
                            gSounds['no-select'].play()
                    else:
                        g_state_manager.Change('serve', {
                            'paddle': self.paddle,
                            'level': self.level,  # Move to the next level
                            'bricks': self.bricks,  # Use the new map for the next level
                            'health': self.health,
                            'score': self.score,
                            'high_scores': self.high_scores,
                            'recover_points': self.recover_points,
                        })
    
    def render(self, screen):
        t_upgrade = gFonts['medium'].render("Upgrade Store: " + str(self.level - 1), False, (255, 255, 255))
        rect = t_upgrade.get_rect(center=(WIDTH/2, 38))
        screen.blit(t_upgrade, rect)

        self.upgrade.render(screen)

        t_skill1 = gFonts['small'].render(f"Ball Damage Level: ", False, (255, 255, 255))
        rect = t_skill1.get_rect(center=(WIDTH/2, 150))
        screen.blit(t_skill1, rect)
        t1_skill1 = gFonts['small'].render(f"Upgrade Cost:", False, (255, 255, 255))
        rect = t1_skill1.get_rect(center=(WIDTH/2, 175))
        screen.blit(t1_skill1, rect)
        t2_skill1 = gFonts['small'].render(f"{self.paddle.item1_level}", False, (210, 125, 44))
        rect = t2_skill1.get_rect(center=(WIDTH/2 + 150, 150))
        screen.blit(t2_skill1, rect)
        t3_skill1 = gFonts['small'].render(f"{self.item1_cost}", False, (210, 125, 44))
        rect = t3_skill1.get_rect(center=(WIDTH/2 + 150, 175))
        screen.blit(t3_skill1, rect)

        t_skill2 = gFonts['small'].render(f"Bomb Ball Level: ", False, (255, 255, 255))
        rect = t_skill2.get_rect(center=(WIDTH/2, 275))
        screen.blit(t_skill2, rect)
        t1_skill2 = gFonts['small'].render(f"Upgrade Cost:", False, (255, 255, 255))
        rect = t1_skill2.get_rect(center=(WIDTH/2, 300))
        screen.blit(t1_skill2, rect)
        t2_skill2 = gFonts['small'].render(f"{self.paddle.item2_level}", False, (210, 125, 44))
        rect = t2_skill2.get_rect(center=(WIDTH/2 + 150, 275))
        screen.blit(t2_skill2, rect)
        t3_skill2 = gFonts['small'].render(f"{self.item2_cost}", False, (210, 125, 44))
        rect = t3_skill2.get_rect(center=(WIDTH/2 + 150, 300))
        screen.blit(t3_skill2, rect)

        t_skill3 = gFonts['small'].render(f"Penetrate Ball Level: ", False, (255, 255, 255))
        rect = t_skill3.get_rect(center=(WIDTH/2, 400))
        screen.blit(t_skill3, rect)
        t1_skill3 = gFonts['small'].render(f"Upgrade Cost:", False, (255, 255, 255))
        rect = t1_skill3.get_rect(center=(WIDTH/2, 425))
        screen.blit(t1_skill3, rect)
        t2_skill3 = gFonts['small'].render(f"{self.paddle.item3_level}", False, (210, 125, 44))
        rect = t2_skill3.get_rect(center=(WIDTH/2 + 150, 400))
        screen.blit(t2_skill3, rect)
        t3_skill3 = gFonts['small'].render(f"{self.item3_cost}", False, (210, 125, 44))
        rect = t3_skill3.get_rect(center=(WIDTH/2 + 150, 425))
        screen.blit(t3_skill3, rect)

        t_skill4 = gFonts['small'].render(f"Companion Level: ", False, (255, 255, 255))
        rect = t_skill4.get_rect(center=(WIDTH/2, 530))
        screen.blit(t_skill4, rect)
        t1_skill4 = gFonts['small'].render(f"Upgrade Cost:", False, (255, 255, 255))
        rect = t1_skill4.get_rect(center=(WIDTH/2, 550))
        screen.blit(t1_skill4, rect)
        t2_skill4 = gFonts['small'].render(f"{self.paddle.item4_level}", False, (210, 125, 44))
        rect = t2_skill4.get_rect(center=(WIDTH/2 + 150, 530))
        screen.blit(t2_skill4, rect)
        t3_skill4 = gFonts['small'].render(f"{self.item4_cost}", False, (210, 125, 44))
        rect = t3_skill4.get_rect(center=(WIDTH/2 + 150, 550))
        screen.blit(t3_skill4, rect)

        t_points = gFonts['small'].render(f'Your Points: {self.paddle.upgrade_point}', False, (255, 255, 255))
        rect = t_points.get_rect(center=(WIDTH/2, 680))
        screen.blit(t_points, rect)