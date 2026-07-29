# author: daniel
# date: 20260618
# location: shanghai
# create the alien class

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """class Alien represents an alien"""
    def __init__(self, ai_game):
        """initialize the alien and set its position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # load the alien image and set its rect properties
        self.image = pygame.image.load('images/alien1.png')
        self.rect = self.image.get_rect()

        # set the location of the alien at the top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store the specific location of the alien
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.x_speed = self.settings.alien_speed_x
        self.y_speed = self.settings.alien_speed_y
        self.x_direction = self.settings.alien_direction_x
        self.y_direction = self.settings.alien_direction_y

        self.alien_level = 1
        self.alien_blood = 1

    def check_edges(self):
        """if alien moved to the edge of the screen in x direction, return True"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def change_direction_x(self):
        self.x_direction = -1 * self.x_direction

    def update(self):
        """move the alien down"""
        self.y += self.y_speed * self.y_direction
        self.rect.y = self.y

        self.x += self.x_speed * self.x_direction
        self.rect.x = self.x

    def set_level(self, level):
        """set the alien level"""
        self.level = level
        self.image = pygame.image.load(f"images/alien{self.level}.png")
        self.alien_blood = level

    def update_blood(self, blood):
        """update the blood"""
        self.alien_blood += blood

    def is_die(self):
        """check if the alien is dead"""
        return self.alien_blood <= 0