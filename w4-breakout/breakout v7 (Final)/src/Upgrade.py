import pygame
from src.constants import *
from src.Dependency import *
import random
import math

class Upgrade:
    def __init__(self):
        self.select = 0
        self.image = upgrade_image_list[self.select]
        self.item1_cost = 1
        self.item2_cost = 1
        self.item3_cost = 1
        self.item4_cost = 1

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if self.select < 4:
                        self.select += 1
                        self.image = upgrade_image_list[self.select]
                elif event.key == pygame.K_UP:
                    if self.select > 0:
                        self.select -= 1
                        self.image = upgrade_image_list[self.select]
                

    def render(self, screen):
        screen.blit(self.image, (WIDTH/2 - 311, HEIGHT/2 - 290))
        screen.blit(upgrade_icon_image_list[0], (385, 125))
        screen.blit(upgrade_icon_image_list[1], (385, 250))
        screen.blit(upgrade_icon_image_list[2], (385, 375))
        screen.blit(upgrade_icon_image_list[3], (385, 500))

    def calculate_gain_point(level, score):
        if level < 11:
            return score//1000 + random.randint(1, 3)
        elif level < 21:
            return score//1000 + random.randint(4, 6)
        else:
            return score//1000 + random.randint(7, 9)
        
    def calculate_upgrade_cost(self, item_level, level):
        base_cost = 2
        
        if level < 11:
            if item_level == 0:
                return 1
            else:
                # Adding randomness to the cost calculation
                item_cost = math.floor(base_cost * random.uniform(1.1, 1.5) * (item_level * random.randint(1, 3)))
                return item_cost

        elif level < 21:
            # Increase base cost for higher levels and add randomness
            item_cost = math.floor(base_cost * random.uniform(1.3, 1.7) * (item_level * random.randint(1.5, 3.5)))
            return item_cost

        else:
            # Highest cost for the highest levels with randomness
            item_cost = math.floor(base_cost * random.uniform(1.5, 2) * (item_level * random.randint(2, 4.5)))
            return item_cost


