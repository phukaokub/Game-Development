import pygame


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
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.on_collide = None
        self.is_thrown = False
        self.velocity_x = 0
        self.velocity_y = 0

        self.start_x = None
        self.start_y = None

        self.powerup = None

    def update(self, dt):
        # If object is thrown, update its position
        self.rect.x = self.x
        self.rect.y = self.y
        if self.is_thrown:
            if self.start_x is None and self.start_y is None:
                self.start_x = self.x
                self.start_y = self.y
            self.state = "thrown"
            self.x += self.velocity_x
            self.y += self.velocity_y

    def render(self, player, screen, adjacent_offset_x, adjacent_offset_y):
        if self.state == "maxlifted":
            self.x = player.x
            self.y = player.y - player.height + 28
            screen.blit(self.image[self.state_list[self.state]],
                        (self.x, self.y))
            screen.blit(self.powerup.image[self.powerup.state_list[self.powerup.state]],
                        (self.x, self.y))
        elif self.state == "thrown":
            screen.blit(self.image[self.state_list[self.state]],
                        (self.x, self.y))
        else:
            screen.blit(self.image[self.state_list[self.state]],
                        (self.x + adjacent_offset_x, self.y + adjacent_offset_y))

        # render pot hitbox
        # pygame.draw.rect(screen, (255, 0, 255), pygame.Rect(self.x, self.y, self.width, self.height))

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def throw(self, direction, speed):
        self.is_thrown = True
        self.y += 64
        if direction == 'left':
            self.velocity_x = -speed
            self.velocity_y = 0
            self.x -= 16
        elif direction == 'right':
            self.velocity_x = speed
            self.velocity_y = 0
            self.x += 16
        elif direction == 'up':
            self.velocity_x = 0
            self.velocity_y = -speed
            self.y -= 32
        elif direction == 'down':
            self.velocity_x = 0
            self.velocity_y = speed
            self.y += 32
