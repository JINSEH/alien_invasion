import pygame
from pygame.sprite import Sprite
import random

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game, source = 'ship'):
        #Create a bullet object at the ships current position
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.colour = self.settings.bullet_colour
        self.source = source
        

        #create a bullet rect at (0,0) and then set correct position
        self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height)
        
        #Different rect positions depending on source
        if source == "ship":
            self.rect.midtop = ai_game.ship.rect.midtop

        elif source == "alien":
            self.rect.midbottom = ai_game.aliens.sprites()[0].rect.midbottom

        #Store the bullet's position as a float
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen"""
        #Update the exact position of the bullet depending on the source
        if self.source == "ship":
            self.y -= self.settings.bullet_speed
        elif self.source == "alien":
            self.y += self.settings.bullet_speed

        #update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.colour, self.rect)
        
