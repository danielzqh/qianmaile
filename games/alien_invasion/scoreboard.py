# author: daniel
# date: 20260618
# location: shanghai
# the scoreboard class used to manage the scores

import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    """indicate the score of the game"""
    def __init__(self, ai_game):
        """initialize the scores and its properties"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # the font setting used for display the scores
        self.text_color = (30, 30, 30)
        self.font = pygame.font.Font(None, 48)

        # draw and render the four images
        self.prep_images()

    def prep_images(self):
        """prepare the images for ships, level, highest score, score"""
        # prepare for the initial scores
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """make the score render as image"""
        rounded_score = round(self.stats.score, 0)
        score_str = f"Score:{rounded_score:,}"
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # indicate the scores at the top right
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = self.screen_rect.centerx + 100
        self.score_rect.top = 20

    def prep_high_score(self):
        """make the high score render as image"""
        high_score = round(self.stats.high_score, 0)
        high_score_str = f"Highest Score:{high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # place the high score at the top middle
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def show_score(self):
        """display the score on the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """check if reached the highest score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """make the level render as image"""
        level_str = "Level:"+ str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # place the level at the bottom of the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = self.score_rect.top

    def prep_ships(self):
        """indicates the number of ships left in the screen"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)