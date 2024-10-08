import pygame
from src.Util import SpriteManager
from src.StateMachine import StateMachine

g_state_manager = StateMachine()

sprite_collection = SpriteManager().spriteCollection

s_paddle_image_list = [sprite_collection["p_blue_1"].image, sprite_collection["p_green_1"].image,
                     sprite_collection["p_red_1"].image, sprite_collection["p_purple_1"].image]

paddle_image_list = [sprite_collection["p_blue_2"].image, sprite_collection["p_green_2"].image,
                     sprite_collection["p_red_2"].image, sprite_collection["p_purple_2"].image]

ball_image_list = [sprite_collection["blue_ball"].image, sprite_collection["green_ball"].image,
                                sprite_collection["red_ball"].image, sprite_collection["purple_ball"].image,
                                sprite_collection["gold_ball"].image, sprite_collection["gray_ball"].image,
                                sprite_collection["last_ball"].image]

gFonts = {
        'small': pygame.font.Font('w4-breakout/breakout v1 (Sprite, paddle, ball)/fonts/font.ttf', 24),
        'medium': pygame.font.Font('w4-breakout/breakout v1 (Sprite, paddle, ball)/fonts/font.ttf', 48),
        'large': pygame.font.Font('w4-breakout/breakout v1 (Sprite, paddle, ball)/fonts/font.ttf', 96)
}

gSounds = {
    'confirm': pygame.mixer.Sound('w4-breakout/breakout v1 (Sprite, paddle, ball)/sounds/confirm.wav'),
    'paddle-hit': pygame.mixer.Sound('w4-breakout/breakout v1 (Sprite, paddle, ball)/sounds/paddle_hit.wav'),
    'pause': pygame.mixer.Sound('w4-breakout/breakout v1 (Sprite, paddle, ball)/sounds/pause.wav'),
    'recover': pygame.mixer.Sound('w4-breakout/breakout v1 (Sprite, paddle, ball)/sounds/recover.wav'),
    'victory': pygame.mixer.Sound('w4-breakout/breakout v1 (Sprite, paddle, ball)/sounds/victory.wav'),
    'hurt': pygame.mixer.Sound('w4-breakout/breakout v1 (Sprite, paddle, ball)/sounds/hurt.wav'),
    'select': pygame.mixer.Sound('w4-breakout/breakout v1 (Sprite, paddle, ball)/sounds/select.wav'),
    'no-select': pygame.mixer.Sound('w4-breakout/breakout v1 (Sprite, paddle, ball)/sounds/no-select.wav'),
    'wall-hit': pygame.mixer.Sound('w4-breakout/breakout v1 (Sprite, paddle, ball)/sounds/wall_hit.wav'),
    'high-score': pygame.mixer.Sound('w4-breakout/breakout v1 (Sprite, paddle, ball)/sounds/high_score.wav'),
    'brick-hit1': pygame.mixer.Sound('w4-breakout/breakout v1 (Sprite, paddle, ball)/sounds/brick-hit-1.wav'),
    'brick-hit2': pygame.mixer.Sound('w4-breakout/breakout v1 (Sprite, paddle, ball)/sounds/brick-hit-2.wav'),
    
}

brick_image_list = [sprite_collection["b_blue_1"].image, sprite_collection["b_blue_2"].image,
                   sprite_collection["b_blue_3"].image, sprite_collection["b_blue_4"].image,
                   sprite_collection["b_green_1"].image, sprite_collection["b_green_2"].image,
                   sprite_collection["b_green_3"].image, sprite_collection["b_green_4"].image,
                   sprite_collection["b_red_1"].image, sprite_collection["b_red_2"].image,
                   sprite_collection["b_red_3"].image, sprite_collection["b_red_4"].image,
                   sprite_collection["b_purple_1"].image, sprite_collection["b_purple_2"].image,
                   sprite_collection["b_purple_3"].image, sprite_collection["b_purple_4"].image,
                   sprite_collection["b_orange_1"].image, sprite_collection["b_orange_2"].image,
                   sprite_collection["b_orange_3"].image, sprite_collection["b_orange_4"].image,
                   sprite_collection["b_gray"].image]
