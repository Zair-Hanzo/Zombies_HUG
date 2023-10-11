import pygame
from pygame.sprite import  Sprite

class Zombie(Sprite):
    def __init__(self, zomb):
        super().__init__()
        self.screen = zomb.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = zomb.settings

        self.image = pygame.image.load("images/scary.png")
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        
    def check_edges(self):
        """Return True if zombie at edge of screen"""
        if self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
            return True
    
    def update(self):
        """ Move the zombie right or left. """
        self.x += (self.settings.zombie_speed * 
                   self.settings.crowd_direction)
        self.rect.x = self.x

    def check_bottom(self):
        if self.rect.top >= self.screen_rect.bottom or self.rect.bottom <= 0:
            return True