
class GameObject:
    def __init__(self, conf, x, y):
        self.type = conf.type

        self.image = conf.image
        self.frame = conf.frame

        # obstacle
        self.solid = conf.solid

        self.default_state = conf.default_state
        self.state = self.default_state
        self.state_list = conf.state_list

        self.x = x
        self.y = y
        self.width = conf.width
        self.height = conf.height

        self.on_collide = None
        #there can be on_attack


    def update(self, dt):
        pass

    def render(self, screen, adjacent_offset_x, adjacent_offset_y):
        screen.blit(self.image[self.state_list[self.state]], (self.x + adjacent_offset_x, self.y + adjacent_offset_y))
