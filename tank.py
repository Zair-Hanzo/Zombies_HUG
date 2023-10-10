import pygame

from settings import Settings

class Tank:
    def __init__(self, tk):
        self.screen = tk.screen
        self.screen_rect = tk.screen.get_rect()
        self.settings = Settings()

        self.image = pygame.image.load("images/tank.png")
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

    def update_tank(self):
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.tank_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.tank_speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.tank_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.tank_speed
        
        self.rect.x = self.x
        self.rect.y = self.y

    def blittank(self):
        self.screen.blit(self.image, self.rect)
