from src.recourses import *
class ObjectConf:
    def __init__(self, type, img, frame, solid, default_state, states, width, height):
        self.type = type
        self.image = img
        self.frame = frame
        self.solid = solid
        self.default_state = default_state
        self.state_list = states
        self.width = width
        self.height = height

        self.direction = None

    #ObjectConf('switch')

GAME_OBJECT_DEFS = {
    'switch': ObjectConf('switch', gSwitch_image_list, 2, False, "unpressed", {'unpressed': 1, 'pressed': 0}, width=48, height=48),
    'pot': ObjectConf('pot', gPot_image_list, 3, False, "default", {'default': 14, 'maxlifted': 33, 'destroyed': 52, 'thrown': 14}, width=48, height=48),
    'atkUp': ObjectConf('atkUp', gPowerup_image_list, 1, False, "default", {'default': 24}, width=16, height=16),
    'heal': ObjectConf('heal', gPowerup_image_list, 1, False, "default", {'default': 32}, width=16, height=16),
    'increase_level': ObjectConf('increase_level', gPowerup_image_list, 1, False, "default", {'default': 27}, width=16, height=16),
    'bucket': ObjectConf('bucket', gBucket_image_list, 1, False, "default", {'default': 110}, width=48, height=48),
}
