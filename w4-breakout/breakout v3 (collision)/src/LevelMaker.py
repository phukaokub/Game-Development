import random, pygame, math
from src.Brick import Brick

class LevelMaker:
    def __init__(self):
        pass

    @classmethod
    def CreateMap(cls, level):
        bricks = []

        # Not gooood enough!!
        num_rows = random.randint(1, 5)
        num_cols = random.randint(7, 13)

        for y in range(num_rows):
            for x in range(num_cols):
                b = Brick(x*96+24 + (13-num_cols) * 48, y*48)
                #b = Brick(x * 32 + 8 + (13 - num_cols) * 16, y * 48)

                bricks.append(b)

        return bricks