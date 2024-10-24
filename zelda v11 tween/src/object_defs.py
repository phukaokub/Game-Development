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

#ObjectConf('switch')


GAME_OBJECT_DEFS = {
    'switch': ObjectConf('switch', gSwitch_image_list, 2, False, "unpressed", {'unpressed':1, 'pressed':0}, width=48, height=48),
    'pot': {

    }
}