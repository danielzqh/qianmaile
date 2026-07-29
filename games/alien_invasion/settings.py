# author: daniel
# date: 20260617
# settings class to store and manage all the settings for the alien invasion game

class Settings:
    """class for store alien invasion game all the settings"""
    def __init__(self):
        """initialize the game settings"""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_limit = 3

        # settings for bullet
        self.bullet_width = 9
        self.bullet_height = 9
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 8

        # settings for alien
        self.fleet_drop_speed = 10

        # use the scale to increase the speed of the game
        self.speedup_scale = 1.1

        # use the scale to increase the speed of the score
        self.score_scale = 1.0

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """initialize the game settings"""
        self.ship_speed = 5.5
        self.bullet_speed = 6.5
        self.alien_speed = 1.0
        self.alien_speed_x = 1.0
        self.alien_speed_y = 1.0
        self.alien_direction_x = 0
        self.alien_direction_y = 1.0

        # fleet_direction 1 indicate moving to the right, -1 indicate moving to the left
        self.fleet_direction = 1

        # score settings
        self.alien_points = 20

    def increase_speed(self):
        """increase the speed of the ships"""
        # self.ship_speed *= self.speedup_scale
        # self.bullet_speed *= self.speedup_scale
        # self.alien_speed *= self.speedup_scale
        self.alien_speed_x *= self.speedup_scale
        self.alien_speed_y *= self.speedup_scale

        self.alien_speed_x = min(self.alien_speed_x, self.alien_speed * 2)
        self.alien_speed_y = min(self.alien_speed_y, self.alien_speed * 2)

        self.alien_points = int(self.alien_points * self.score_scale)