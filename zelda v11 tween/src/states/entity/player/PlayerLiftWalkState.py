from src.constants import *
from src.states.entity.player.PlayerWalkState import PlayerWalkState
import pygame, time

class PlayerLiftWalkState(PlayerWalkState):
    def __init__(self, player, dungeon):
        super(PlayerLiftWalkState, self).__init__(player, dungeon)

        self.entity.ChangeAnimation('lift_walk_'+self.entity.direction)
        self.dungeon = dungeon  