from src.states.entity.EntityIdleState import EntityIdleState
import pygame


class PlayerIdleState(EntityIdleState):
    def __init__(self, player):
        super(PlayerIdleState, self).__init__(player)
        self.player = player

    def Enter(self, params):
        self.entity.offset_y = 15
        self.entity.offset_x = 0
        super().Enter(params)
        if self.player.is_lift:
            print('Enter lift idle')
            print(self.entity.direction)
            self.entity.ChangeAnimation('lift_walk_'+self.entity.direction)
            

    def Exit(self):
        pass

    def update(self, dt, events):
        pressedKeys = pygame.key.get_pressed()
        if pressedKeys[pygame.K_LEFT] or pressedKeys [pygame.K_RIGHT] or pressedKeys [pygame.K_UP] or pressedKeys [pygame.K_DOWN]:
            self.entity.ChangeState('walk')

        for event in events:
            if event.type == pygame.KEYDOWN:
                print('player is lift = ', self.player.is_lift)
                if self.player.is_lift:
                    if event.key == pygame.K_SPACE:
                        self.entity.ChangeState('throw')
                else:
                    if event.key == pygame.K_SPACE:
                        self.entity.ChangeState('swing_sword')
                    elif event.key == pygame.K_f:
                        self.entity.ChangeState('lift')
