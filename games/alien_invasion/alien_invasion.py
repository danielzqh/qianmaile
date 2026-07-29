# author: daniel
# date: 20260617
# game for alien invasion

import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from random import randint, uniform
import random
import time

class AlienInvasion():
    """alien invasion class for manage game resources and behavior"""
    def __init__(self):
        """initialize alien invasion class"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        # create an instance for game statistics to store the data information when playing
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        # self._create_fleet()

        # game start up at active state
        self.game_active = False

        # create the play button
        self.play_button = Button(self, "Play")

        # number of aliens missed, will add to the number of aliens created for the new fleet
        self.num_of_aliens_missed = 0

        # clock to remember start time of each level, will start a new level after 5 seconds lapsed for each level
        self.timer = int(time.time())

        # clock to remember the start time of unbeatable
        self.timer_unbeatable = None

    def _create_fleet(self):
        """create a fleet of aliens and add them to the aliens group"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        speed_x = alien.x_speed
        speed_y = alien.y_speed
        x_direction = alien.x_direction # a float value in [-1.0,1.0], negative means to left, positive means to right
        y_direction = alien.y_direction # a float value for scale the direction y speed

        num_of_aliens = self.stats.level
        num_of_aliens = min(num_of_aliens, 12)
        num_of_aliens += self.num_of_aliens_missed

        num_of_aliens_l2 = int(num_of_aliens / 4)
        num_of_aliens_l3 = int(num_of_aliens / 13)
        aliens_l2_idx = random.sample(range(num_of_aliens), num_of_aliens_l2)
        aliens_l3_idx = random.sample(aliens_l2_idx, num_of_aliens_l3)

        step = int((self.settings.screen_width - 3 * alien_width) / num_of_aliens)
        for i in range (num_of_aliens):
            x = randint(current_x, current_x + step)
            x_direction = uniform(-1.0, 1.0)
            y_direction = uniform(0.5,1.3)
            self._create_alien(x, current_y, speed_x, x_direction, speed_y, y_direction, 1)
            if i in aliens_l2_idx:
                self._create_alien(x, current_y, speed_x, x_direction, speed_y, y_direction, 2)
            if i in aliens_l3_idx:
                self._create_alien(x, current_y, speed_x, x_direction, speed_y, y_direction, 3)
            current_x += step


    def _create_alien(self, x_position, y_position, x_speed, x_direction, y_speed, y_direction, level):
        """create an alien and add it to the aliens group"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        new_alien.x_speed = x_speed
        new_alien.y_speed = y_speed
        new_alien.x_direction = x_direction
        new_alien.y_direction = y_direction
        if level > 1:
            new_alien.set_level(level)
        self.aliens.add(new_alien)

    def run_game(self):
        """run the game"""
        while True:
            # listen to keyboard and mouse event
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """response to keyboard and mouse events"""
        for event in pygame.event.get(): # might have multiple events in one capture, eg. multiple bullets at same location
            if event.type == pygame.QUIT:
                self.stats.save_stats()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """start a new game when player clicked the Play button"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self._start_game()


    def _check_keydown_events(self, event):
        """keydown pressed"""
        # print(event.key)
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_q:
            self.stats.save_stats()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p and not self.game_active:
            self._start_game()

    def _start_game(self):
        """start the game"""
        # reset the game's statistics info
        self.stats.reset_stats()
        self.game_active = True

        # remove the alien and bullet list
        self.bullets.empty()
        self.aliens.empty()

        self.num_of_aliens_missed = 0
        # create a new alien fleet, place the ship on the bottom middle
        self._create_fleet()
        self.ship.center_ship()

        # hide the mouse cursor
        pygame.mouse.set_visible(False)

        # reset the settings
        self.settings.initialize_dynamic_settings()

        # reset the stats and scores
        self.stats.reset_stats()
        self.sb.prep_images()

        self.timer = int(time.time())
        if self.timer_unbeatable:
            self.timer_unbeatable = None
            self.ship.set_state(1)

    def _check_keyup_events(self, event):
        """keyup release"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False

    def _fire_bullet(self):
        """create a bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """update the bullets location and remove the disappeared bullets"""
        # update the location of the bullets
        self.bullets.update()
        # remove the disappeared bullets saving some memory
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # check whether any bullets hit any aliens
        # if the answer yes, remove the bullets and aliens accordingly
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, False)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                for alien in aliens:
                    alien.update_blood(-1)
                    if alien.is_die():
                        self.aliens.remove(alien)

            self.sb.prep_score()
            self.sb.check_high_score()


        if not self.aliens or int(time.time()) - self.timer > 5: # if the level lapsed 5 seconds or more, start a new level automatically
            self._start_new_level()

    def _start_new_level(self):
        """start a new level"""
        # remove all the bullets and create a new fleet
        # self.bullets.empty()
        self.settings.increase_speed()

        # increase the level
        self.stats.level += 1
        self.sb.prep_level()

        self._create_fleet()
        self.num_of_aliens_missed = 0
        self.timer = int(time.time())
        if self.timer_unbeatable and self.timer - self.timer_unbeatable > 3:
            self.timer_unbeatable = None
            self.ship.set_state(1)

    def _update_aliens(self):
        """update the location of the aliens"""
        self._check_fleet_edges()
        self.aliens.update()

        # inspect the collision between alien and ship
        if not self.timer_unbeatable and pygame.sprite.spritecollide(self.ship, self.aliens, True):
            self._ship_hit()

        # check whether any alien moved to the bottom of the screen
        self._check_aliens_bottom()

    def _ship_hit(self):
        """when ship and alien collide"""
        if self.stats.ships_left > 0:
            # reduce the ships left by 1
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # empty the aliens and bullets
            # self.bullets.empty()
            # self.aliens.empty()
            # self.num_of_aliens_missed = 0

            # create a new alien fleet, move the ship to the center bottom
            # self._create_fleet()
            # self.ship.center_ship()

            # pause
            # sleep(3)
            self.timer = int(time.time())
            self.timer_unbeatable = self.timer
            self.ship.set_state(2)

        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """check whether the aliens reached the bottom of the screen"""
        for alien in self.aliens.copy():
            if alien.rect.top >= self.settings.screen_height:
                # just like the ship been hit
                # self._ship_hit()
                # break
                self.aliens.remove(alien)
                self.num_of_aliens_missed += 1

    def _check_fleet_edges(self):
        """while aliens moved to the edge take the action accordingly"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                #self._change_fleet_direction()
                #break
                alien.change_direction_x()

    # def _change_fleet_direction(self):
    #     """move the whole fleet down and change its direction"""
    #     for alien in self.aliens.sprites():
    #         alien.rect.y += self.settings.fleet_drop_speed
    #     self.settings.fleet_direction *= -1

    def _update_screen(self):
        """update the images on the screen and shift to the new screen"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # display the score
        self.sb.show_score()

        if not self.game_active:
            self.play_button.draw_button()
        # to display the game window
        pygame.display.flip()


if __name__ == "__main__":
    # create game instance and run the game
    ai =  AlienInvasion()
    ai.run_game()