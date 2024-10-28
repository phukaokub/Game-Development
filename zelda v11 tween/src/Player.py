from src.EntityBase import EntityBase
from src.Dependencies import *
from src.recourses import *

class Player(EntityBase):
    def __init__(self, conf):
        super(Player, self).__init__(conf)

        self.carrying_object = None
        self.attack = 1
        self.level = 1
        self.difficulty = 1

    def update(self, dt, events):
        super().update(dt, events)

        if self.level == 1:
            self.attack += 0
        elif self.level == 5:
            self.attack += 1
        elif self.level == 10:
            self.attack += 2

    def Collides(self, target):
        y, height = self.y + self.height/2, self.height-self.height/2

        return not (self.x + self.width < target.x or self.x > target.x + target.width or
                    y + height < target.y or y > target.y + target.height)


    def render(self):
        super().render()

    def CreateAnimations(self):
        self.animation_list = gPlayer_animation_list