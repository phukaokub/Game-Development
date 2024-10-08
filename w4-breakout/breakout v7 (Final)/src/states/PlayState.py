import random, pygame, sys
from src.states.BaseState import BaseState
from src.constants import *
from src.Explode import Explode
from src.Dependency import *
import src.CommonRender as CommonRender

class PlayState(BaseState):
    def __init__(self):
        super(PlayState, self).__init__()
        self.paused = False
        self.skip = False

    def Enter(self, params):
        self.paddle = params['paddle']
        self.bricks = params['bricks']
        self.health = params['health']
        self.score = params['score']
        self.high_scores = params['high_scores']
        self.ball = params['ball']
        self.level = params['level']

        self.recover_points = 5000

        self.ball.dx = random.randint(-600, 600)  # -200 200
        self.ball.dy = random.randint(-180, -150)

        self.powerups = []
        self.explosions = []
        self.penBall = None

    def update(self,  dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                    gSounds['pause'].play()
                    #music_channel.play(sounds_list['pause'])
                if event.key == pygame.K_UP:
                    g_state_manager.Change('victory', {
                        'level':self.level,
                        'paddle':self.paddle,
                        'health':self.health,
                        'score':self.score,
                        'high_scores':self.high_scores,
                        'ball':self.ball,
                        'recover_points':self.recover_points
                    })
                    #music_channel.play(sounds_list['pause'])

        if self.paused:
            return

        self.paddle.update(dt)
        self.ball.update(dt)
        if self.penBall:
            self.penBall.update(dt)
        for explosion in self.explosions[:]:
            explosion.update(dt)
            del self.explosions[0]

        # Update powerups
        for powerup in self.powerups[:]:  # Iterate over a copy of the list
            powerup.update(dt)
            check = powerup.check_collision_with_paddle(self.paddle)
            if check:
                if powerup.type == 0:
                    self.paddle.powerup_list.append("Bomb")
                elif powerup.type == 1:
                    self.paddle.powerup_list.append("Penetrate")

            # Remove powerup if it goes off the screen or is consumed
            if not powerup.alive:
                self.powerups.remove(powerup)

        # update ball to powerup
        if self.ball.Collides(self.paddle):
            # check ball type
            if self.paddle.powerup_list:
                if "Bomb" in self.paddle.powerup_list[0]:
                    del self.paddle.powerup_list[0]
                    self.ball.type = 1
                elif "Penetrate" in self.paddle.powerup_list[0]:
                    del self.paddle.powerup_list[0]
                    self.ball.type = 2
                    return
                
            # raise ball above paddle
            ####can be fixed to make it natural####
            self.ball.rect.y = self.paddle.rect.y - 24
            self.ball.dy = -self.ball.dy

            # half left hit while moving left (side attack) the more side, the faster
            if self.ball.rect.x + self.ball.rect.width < self.paddle.rect.x + (self.paddle.width / 2) and self.paddle.dx < 0:
                self.ball.dx = -150 + -(8 * (self.paddle.rect.x + self.paddle.width / 2 - self.ball.rect.x))
            # right paddle and moving right (side attack)
            elif self.ball.rect.x > self.paddle.rect.x + (self.paddle.width / 2) and self.paddle.dx > 0:
                self.ball.dx = 150 + (8 * abs(self.paddle.rect.x + self.paddle.width / 2 - self.ball.rect.x))
            gSounds['paddle-hit'].play()

        for k, brick in enumerate(self.bricks):
            if brick.alive and self.ball.Collides(brick):
                previous_tier = brick.tier
                previous_color = brick.color
                new_powerup, self.penBall, explosion = brick.Hit(self.paddle, self.ball)
                if new_powerup:
                    self.powerups.append(new_powerup)
                if explosion:
                    self.explosions.append(explosion)
                self.score = self.calculateScore(brick, previous_tier, previous_color)

                if self.score > self.recover_points:
                    self.health = min(3, self.health + 1)
                    self.recover_points = min(100000, self.recover_points * 2)

                    gSounds['recover'].play()
                    #music_channel.play(sounds_list['recover'])

                if self.CheckVictory() or self.skip:
                    gSounds['victory'].play()

                    g_state_manager.Change('victory', {
                        'level':self.level,
                        'paddle':self.paddle,
                        'health':self.health,
                        'score':self.score,
                        'high_scores':self.high_scores,
                        'ball':self.ball,
                        'recover_points':self.recover_points
                    })
                if explosion:
                    # Apply explosion effect to nearby bricks
                    for b in self.bricks:
                        if b.alive and explosion.is_within_radius(b.rect.x + b.width // 2, b.rect.y + b.height // 2):
                            # Apply damage to the brick
                            b.Hit(self.paddle, self.ball)
                    
                    # Add the explosion to the list of explosions
                    self.explosions.append(explosion)

                # hit brick from left while moving right -> x flip
                if self.ball.rect.x + 6 < brick.rect.x and self.ball.dx > 0:
                    self.ball.dx = -self.ball.dx
                    self.ball.rect.x = brick.rect.x - 24

                # hit brick from right while moving left -> x flip
                elif self.ball.rect.x + 18 > brick.rect.x + brick.width and self.ball.dx < 0:
                    self.ball.dx = -self.ball.dx
                    self.ball.rect.x = brick.rect.x + 96

                # hit from above -> y flip
                elif self.ball.rect.y < brick.rect.y:
                    self.ball.dy = -self.ball.dy
                    self.ball.rect.y = brick.rect.y - 24

                # hit from bottom -> y flip
                else:
                    self.ball.dy = -self.ball.dy
                    self.ball.rect.y = brick.rect.y + 48

                # whenever hit, speed is slightly increase, maximum is 450
                if abs(self.ball.dy) < 450:
                    self.ball.dy = self.ball.dy * 1.02

                break
            elif brick.alive and self.penBall and self.penBall.Collides(brick):
                previous_tier = brick.tier
                previous_color = brick.color
                brick.Hit(self.paddle, self.penBall)
                self.score = self.calculateScore(brick, previous_tier, previous_color)

                if self.score > self.recover_points:
                    self.health = min(3, self.health + 1)
                    self.recover_points = min(100000, self.recover_points * 2)

                    gSounds['recover'].play()
                    #music_channel.play(sounds_list['recover'])

                if self.CheckVictory() or self.skip:
                    gSounds['victory'].play()

                    g_state_manager.Change('victory', {
                        'level':self.level,
                        'paddle':self.paddle,
                        'health':self.health,
                        'score':self.score,
                        'high_scores':self.high_scores,
                        'ball':self.ball,
                        'recover_points': self.recover_points
                    })

                break

        if self.ball.rect.y >= HEIGHT:
            self.health -= 1
            gSounds['hurt'].play()

            if self.health == 0:
                g_state_manager.Change('game-over', {
                    'score':self.score,
                    'high_scores': self.high_scores
                })
            else:
                self.powerups = []
                g_state_manager.Change('serve', {
                    'level': self.level,
                    'paddle': self.paddle,
                    'bricks': self.bricks,
                    'health': self.health,
                    'score': self.score,
                    'high_scores': self.high_scores,
                    'recover_points': self.recover_points
                })
        

    def Exit(self):
        pass

    def render(self, screen):
        for brick in self.bricks:
            brick.render(screen)
        for powerup in self.powerups:
            powerup.render(screen)
        
        if self.penBall:
            if self.penBall.alive:
                self.penBall.render(screen)

        for explosion in self.explosions:
            explosion.render(screen)

        self.paddle.render(screen)
        self.ball.render(screen)

        CommonRender.RenderScore(screen, self.score)
        CommonRender.RenderHealth(screen, self.health)

        if self.paused:
            t_pause = gFonts['large'].render("PAUSED", False, (255, 255, 255))
            rect = t_pause.get_rect(center = (WIDTH/2, HEIGHT/2))
            screen.blit(t_pause, rect)

    def CheckVictory(self):
        for brick in self.bricks:
            if brick.alive:
                return False

        return True

    def calculateScore(self, brick, previous_tier, previous_color):
        # Calculate score based on the difference in tiers and colors before and after the hit
        tier_difference = previous_tier - brick.tier
        color_difference = previous_color - brick.color
        
        # If the brick's tier has changed, add points for both tier and color changes
        if tier_difference > 0:
            self.score += (tier_difference * 200) + ((previous_color - 1 + (5 * tier_difference)) * 25)
        else:
            # If only the color changed, calculate points based on color change
            self.score += color_difference * 25
        
        return self.score

