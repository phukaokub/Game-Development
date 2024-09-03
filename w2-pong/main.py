import pygame, sys, random, math

from constant import *
from Ball import Ball
from Paddle import Paddle
from Item import Item

class GameMain:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.music_channel = pygame.mixer.Channel(0)
        self.music_channel.set_volume(0.2)
        
        self.sounds_list = {
            'paddle_hit': pygame.mixer.Sound('w2-pong/sounds/paddle_hit.wav'),
            'score': pygame.mixer.Sound('w2-pong/sounds/score.wav'),
            'wall_hit': pygame.mixer.Sound('w2-pong/sounds/wall_hit.wav')
        }

        self.small_font = pygame.font.Font('w2-pong/font.ttf', 24)
        self.large_font = pygame.font.Font('w2-pong/font.ttf', 48)
        self.score_font = pygame.font.Font('w2-pong/font.ttf', 96)

        self.player1_score = 0
        self.player2_score = 0

        self.serving_player = 1
        self.winning_player = 0

        self.player1 = Paddle(self.screen, 30, 90, 15, 60, (217,217,217), (128, 0, 0))
        self.player2 = Paddle(self.screen, WIDTH - 30, HEIGHT - 90, 15, 60, (217,217,217), (217, 217, 217))

        self.ball = Ball(self.screen, WIDTH/2 - 6, HEIGHT/2 - 6, 12, 12, (255, 255, 255))

        self.game_state = 'start'

        self.game_level = random.randint(1, 2)
        self.items = []
        self.item_timer = random.randint(5, 10)  # Time in seconds to spawn next item


    def update(self, dt, events):
        # Handle events as before
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_state == 'start':
                        self.game_state = 'serve'
                    elif self.game_state == 'serve':
                        self.game_state = 'play'
                    elif self.game_state == 'done':
                        if self.winning_player == 1:
                            # Transition to Level 2 if Player 1 wins
                            self.game_level = 2
                        self.game_state = 'serve'
                        self.ball.Reset()
                        self.player1_score = 0
                        self.player2_score = 0
                        self.serving_player = 2 if self.winning_player == 1 else 1
                        self.winning_player = 0

        if self.game_state == 'serve':
            self.ball.dy = random.uniform(-150, 150)
            if self.serving_player == 1:
                self.ball.dx = random.uniform(420, 600)
            else:
                self.ball.dx = -random.uniform(420, 600)
            self.player1.reset_paddle_size()
            self.player2.reset_paddle_size()
            self.items.clear()
            self.ball.reset_color()

        elif self.game_state == 'play':
            if self.ball.Collides(self.player1):
                self.ball.dx = -self.ball.dx * 1.03  # reflect speed multiplier
                self.ball.rect.x = self.player1.rect.x + 15
                if self.ball.dy < 0:
                    self.ball.dy = -random.uniform(30, 450)
                else:
                    self.ball.dy = random.uniform(30, 450)
                if self.ball.is_fake == True and self.ball.activate_mirror == self.player1:
                    self.ball.activate_mirror_ball()
                self.music_channel.play(self.sounds_list['paddle_hit'])
                self.player1.reset_paddle_size()
                self.ball.reset_color()

            if self.ball.Collides(self.player2):
                self.ball.dx = -self.ball.dx * 1.03
                self.ball.rect.x = self.player2.rect.x - 12
                if self.ball.dy < 0:
                    self.ball.dy = -random.uniform(30, 450)
                else:
                    self.ball.dy = random.uniform(30, 450)
                if self.ball.is_fake == True and self.ball.activate_mirror == self.player2:
                    self.ball.activate_mirror_ball()
                self.music_channel.play(self.sounds_list['paddle_hit'])
                self.player2.reset_paddle_size()
                self.ball.reset_color()

            if self.ball.rect.y <= 0:
                self.ball.rect.y = 0
                self.ball.dy = -self.ball.dy
                self.music_channel.play(self.sounds_list['wall_hit'])

            if self.ball.rect.y >= HEIGHT - 12:
                self.ball.rect.y = HEIGHT - 12
                self.ball.dy = -self.ball.dy
                self.music_channel.play(self.sounds_list['wall_hit'])

            if self.ball.rect.x < 0:
                self.serving_player = 1
                self.player2_score += 1
                self.music_channel.play(self.sounds_list['score'])
                if self.player2_score == WINNING_SCORE:
                    self.winning_player = 2
                    self.game_state = 'done'
                    self.game_level = 1
                else:
                    self.game_state = 'serve'
                    self.ball.Reset()

            if self.ball.rect.x > WIDTH:
                self.serving_player = 2
                self.player1_score += 1
                self.music_channel.play(self.sounds_list['score'])
                if self.player1_score == WINNING_SCORE:
                    self.winning_player = 1
                    self.game_state = 'done'
                else:
                    self.game_state = 'serve'
                    self.ball.Reset()

            if self.game_level == 1:
                self.player2.weak_AI(self.ball, dt)
            elif self.game_level == 2:
                self.player2.strong_AI(self.ball, dt)

            for self.item in self.items:
                if self.ball.Collides(self.item):
                    self.item.activate(self.ball, self.player1, self.player2)

            self.item_timer -= dt
            if self.item_timer <= 0 and self.items.__len__() < 3:
                self.generate_item()
                self.item_timer = random.randint(2, 5)

            for item in self.items[:]:
                if item.update(self.ball, self.player1, self.player2):  
                    self.items.remove(item)  # Remove item if it has been activated


        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.player1.dy = -PADDLE_SPEED
        elif key[pygame.K_s]:
            self.player1.dy = PADDLE_SPEED
        else:
            self.player1.dy = 0

        # Randomly generate an item over time
        for self.item in self.items:
            if self.game_state == 'play' and not self.item and random.random() < ITEM_SPAWN_CHANCE:
                self.generate_item()
        
        # Check for item collision and activation
        for self.item in self.items:
            if self.item and self.ball.Collides(self.item):
                self.item.activate(self.ball, self.player1, self.player2)
                self.item = None
        
        # Update ball, paddles, and other game elements
        if self.game_state == 'play':
            self.ball.update(dt)
        self.player1.update(dt)
        self.player2.update(dt)

        

    def render(self):
        self.screen.fill((40, 45, 52))

        if self.game_state == 'start':
            t_welcome = self.small_font.render("Welcome to Pong!", False, (255, 255, 255))
            text_rect = t_welcome.get_rect(center=(WIDTH / 2, 30))
            self.screen.blit(t_welcome, text_rect)

            t_press_enter_begin = self.small_font.render('Press Enter to begin!', False, (255, 255, 255))
            text_rect = t_press_enter_begin.get_rect(center=(WIDTH / 2, 60))
            self.screen.blit(t_press_enter_begin, text_rect)

        elif self.game_state == 'serve':
            t_serve = self.small_font.render("player" + str(self.serving_player) + "'s serve!", False, (255, 255, 255))
            text_rect = t_serve.get_rect(center=(WIDTH/2, 30))
            self.screen.blit(t_serve, text_rect)

            t_enter_serve = self.small_font.render("Press Enter to serve!", False, (255, 255, 255))
            text_rect = t_enter_serve.get_rect(center=(WIDTH / 2, 60))
            self.screen.blit(t_enter_serve, text_rect)
            
            if self.game_level == 1:
                t_level = self.small_font.render('Level 1: Weak AI', False, (255, 255, 255))
                text_rect = t_level.get_rect(center=(WIDTH / 2, 90))
                self.screen.blit(t_level, text_rect)
            elif self.game_level == 2:
                t_level = self.small_font.render('Level 2: Strong AI', False, (255, 255, 255))
                text_rect = t_level.get_rect(center=(WIDTH / 2, 90))
                self.screen.blit(t_level, text_rect)

        elif self.game_state == 'play':
            pass
        elif self.game_state == 'done':
            t_win = self.large_font.render("player" + str(self.winning_player) + "'s wins!", False, (255, 255, 255))
            text_rect = t_win.get_rect(center=(WIDTH / 2, 30))
            self.screen.blit(t_win, text_rect)

            t_restart = self.small_font.render("Press Enter to restart", False, (255, 255, 255))
            text_rect = t_restart.get_rect(center=(WIDTH / 2, 70))
            self.screen.blit(t_restart, text_rect)

        self.DisplayScore()

        # Right paddle
        self.player2.render()

        # Left paddle
        self.player1.render()

        # Ball
        self.ball.render()

        # Items
        for item in self.items:
            item.render()


    def DisplayScore(self):
        self.t_p1_score = self.score_font.render(str(self.player1_score), False, (255, 255, 255))
        self.t_p2_score = self.score_font.render(str(self.player2_score), False, (255, 255, 255))
        self.screen.blit(self.t_p1_score, (WIDTH/2 - 150, HEIGHT/3))
        self.screen.blit(self.t_p2_score, (WIDTH / 2 + 90, HEIGHT / 3))

    def generate_item(self):
        x = random.randint(200, WIDTH - 200)
        y = random.randint(100, HEIGHT - 100)
        item_type = random.choice(['mirror_ball', 'speed_ball', 'reduce_paddle_size', 'increase_paddle_size'])
        self.items.append(Item(self.screen, x, y, item_type))

if __name__ == '__main__':
    main = GameMain()

    clock = pygame.time.Clock()

    while True:
        pygame.display.set_caption("Pong game running with {:d} FPS".format(int(clock.get_fps())))

        # elapsed time from the last call
        dt = clock.tick(MAX_FRAME_RATE)/1000.0

        events = pygame.event.get()
        main.update(dt, events)
        main.render()

        pygame.display.update()
