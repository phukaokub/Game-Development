from src.EntityBase import EntityBase
from src.Dependencies import *

class Player(EntityBase):
    def __init__(self, conf):
        super(Player, self).__init__(conf)

    def update(self, dt, events):
        super().update(dt, events)


    def Collides(self, target):
        y, height = self.y + self.height/2, self.height-self.height/2

        return not (self.x + self.width < target.x or self.x > target.x + target.width or
                    y + height < target.y or y > target.y + target.height)


    def render(self):
        super().render()

    def CreateAnimations(self):
        self.animation_list = gPlayer_animation_list