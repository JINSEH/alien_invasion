import pygame
from pygame.sprite import Sprite
from bullet import Bullet

class Alien(Sprite):
    def __init__(self, ai_game):
        """Initialize the alien and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ai_game = ai_game

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load("images/alien.bmp")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

        self.shoot_timer = 0
        self.shoot_interval = 200

        self.initial_first_row_y = ai_game.first_row_y  # Add this line

    def update(self):
        """Move the alien to the right or left"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
        self.shoot_timer += 1

        if self.shoot_timer >= self.shoot_interval and self._is_in_first_row():
            self.shoot_bullet()
            self.shoot_timer = 0

    def shoot_bullet(self):
        """Create a bullet fired by the alien"""
        new_bullet = Bullet(self.ai_game, source="alien")
        new_bullet.rect.midbottom = self.rect.midbottom
        self.ai_game.bullets.add(new_bullet)

    def _is_in_first_row(self):
        """Check if the alien is in the first row"""
        margin = self.rect.height // 2  # Allow half the height of the alien as margin
        return abs(self.rect.y - self.initial_first_row_y) <= margin

    def check_edges(self):
        """Return true if alien is at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
