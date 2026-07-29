# author: daniel
# date: 20260617
# class for bullet

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """manage the class of bullet shot by ship"""

    def __init__(self, ai_game):
        """initialize the bullet instance at the location of the ship"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        """move the bullet up"""
        # update the location of the speed
        self.y -= self.settings.bullet_speed
        # update the bullet location
        self.rect.y = self.y

    def draw_bullet(self):
        """draw the bullet on the screen"""
        # pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.circle(self.screen, self.color, self.rect.center, self.rect.width * 0.8)