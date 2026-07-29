# author: daniel
# date: 20260618
# location: shanghai
# As pygame does not have the button class, we create a button class to simulate the button UI

import pygame.font

class Button:
    """create the button class for the game"""
    def __init__(self, ai_game, msg):
        """initialize the button"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # set the button size and properties
        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font(None, 48)

        # create the rect object for the button and make it center
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # for the message information of the button
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """make the msg as the image, place it on the middle of the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """draw the button with the button color and then draw the text"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)