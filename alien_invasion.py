import sys
import pygame
from time import sleep
from ship import Ship
from settings import Settings
from bullet import Bullet
from alien import Alien
from star import Star
from random import randint
from gamestats import Gamestats
from button import Button
from scoreboard import Scoreboard
from pathlib import Path
import json

class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((1200, 800))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height        
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.star = pygame.sprite.Group()
        self.gamestats = Gamestats(self)
        self.sb = Scoreboard(self)
        self.easy_button = Button(self, "Easy", (500, 300))
        self.medium_button = Button(self, "Medium")
        self.hard_button = Button(self, "Hard", (500, 450))
        self.first_row_y = None  # Add this line

        self._create_fleet()
        self._create_grid_stars()
        self.game_active = False

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(120)

    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """Checks which button has been pressed and assigns difficulty settings"""
        if self.easy_button.rect.collidepoint(mouse_pos) and not self.game_active:
            self.settings.difficulty = "easy"
            self._start_game()
        elif self.medium_button.rect.collidepoint(mouse_pos) and not self.game_active:
            self.settings.difficulty = "medium"
            self._start_game()
        elif self.hard_button.rect.collidepoint(mouse_pos) and not self.game_active:
            self.settings.difficulty = "hard"
            self._start_game()

    def _start_game(self):
        """Initialize game settings when starting a new game"""
        self.settings.initialise_dynamic_settings()
        self.gamestats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.game_active = True
        self.bullets.empty()
        self.aliens.empty()
        self._create_fleet()
        self.ship.center_ship()
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self, source="ship")
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.top >= self.settings.screen_height:
                self.bullets.remove(bullet)
        self._check_bullet_collisions()

    def _check_bullet_collisions(self):
        """Respond to any bullet collisions"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.gamestats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self._start_next_level()

    def _start_next_level(self):
        """Start a new level"""
        self.bullets.empty()
        self.settings.increase_speed()
        self._create_fleet()
        self.gamestats.level += 1
        self.sb.prep_level()
        for alien in self.aliens.sprites():
            alien.shoot_timer = 0

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.gamestats.ships_left > 0:
            self.gamestats.ships_left -= 1
            self.sb.prep_ships()
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """Update the position of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()
        for alien in self.aliens.sprites():
            alien.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_colour)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        self.star.draw(self.screen)
        if not self.game_active:
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()
        pygame.display.flip()

    def _create_fleet(self):
        """Create a fleet of aliens"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        if self.first_row_y is None:
            self.first_row_y = current_y
        while current_y < (self.settings.screen_height - 8 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached the edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        """Check if aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _create_grid_stars(self):
        """Create a grid of stars"""
        star = Star(self)
        star_width, star_height = star.rect.size
        current_x, current_y = star_width, star_height
        while current_y < self.settings.screen_height:
            while current_x < self.settings.screen_width:
                self._create_star(current_x, current_y)
                current_x += randint(100, 200)
            current_x = star_width
            current_y += randint(100, 200)

    def _create_star(self, x_pos, y_pos):
        """Create a star and place it in the row"""
        new_star = Star(self)
        new_star.x = x_pos
        new_star.rect.x = x_pos
        new_star.rect.y = y_pos
        self.star.add(new_star)

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
