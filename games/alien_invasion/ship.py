import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """manage the ship class"""
    def __init__(self, ai_game):
        """initialize the ship and set the initial location"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # load the ship image and get the outer rectangle
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # place the ship at the bottom middle part of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        #self.rect.center = self.screen_rect.center

        # add a floating number for the location as the speed can be floating number
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.state = 1

    def update(self):
        """move the ship position based on the key pressed"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

        if self.moving_up and self.rect.top > self.rect.height:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        self.rect.y = self.y


    def blitme(self):
        """draw the ship at the specified location"""
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        """move the ship to the center bottom"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def set_state(self, state):
        """set the state of the ship, eg. unbeatable or not """
        self.state = state
        self.image = pygame.image.load(f"images/ship{self.state}.png")
