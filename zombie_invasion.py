import pygame

import sys

from settings import Settings
from tank import Tank
from bullets import Bullets
from zombie import Zombie
from random import randint

class Zombie_Invasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Zombie Invasion")
        self.tank = Tank(self)
        self.bullets = pygame.sprite.Group()
        self.zombies = pygame.sprite.Group()
        self._create_crowd()

    def run_game(self):
        while True:
            self._check_events()
            self.tank.update_tank()
            self._update_bullets()
            self._update_zombies()
            self._update_screen()

    
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    def _check_keydown_events(self, event):
        if event.key == pygame.K_UP:
            self.tank.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.tank.moving_down = True
        elif event.key == pygame.K_RIGHT:
            self.tank.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.tank.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_UP:
            self.tank.moving_up = False
        if event.key == pygame.K_DOWN:
            self.tank.moving_down = False
        elif event.key == pygame.K_RIGHT:
            self.tank.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.tank.moving_left = False
    
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullets(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.zombies, False, True
        )
    
    def _update_zombies(self):
        self._check_crowd_edges()
        self.zombies.update()
        self.free_memory()


    def _create_crowd(self):
        zombie = Zombie(self)
        zombie_width, zombie_height = zombie.rect.size
        available_space_x = self.settings.screen_width - (2 * zombie_width)
        zombie_number = available_space_x // (2 * zombie_width)
        available_space_y = self.settings.screen_height - (2 * zombie_height)
        - self.tank.rect.height
        row_number = available_space_y // (2 * zombie_height)
        for row_num in range(row_number):
            for zom_num in range(zombie_number):
                self._create_zombie(row_num, zom_num)
    
    def _create_zombie(self, r_num, z_num):
        zombie = Zombie(self)
        zombie_width, zombie_height = zombie.rect.size
        max_zom = (self.settings.screen_width - (2 * zombie_width)) // (2 * zombie_width)
        max_row = (self.settings.screen_height - (3 * zombie_height)
                    - self.tank.rect.height) // (2 * zombie_height)
        r_num = randint(0, max_row)
        z_num = randint(0, max_zom)
        zombie.x = zombie_width + 2 * zombie_width * z_num
        zombie.rect.x = zombie.x
        zombie.rect.y = zombie_height + 2 * zombie_height * r_num
        self.zombies.add(zombie)

    def _check_crowd_edges(self):
        for zombie in self.zombies.sprites():
            if zombie.check_edges():
                self._change_crowd_direction()
                break
    
    def _change_crowd_direction(self):
        for zombie in self.zombies.sprites():
            zombie.rect.y += self.settings.crowd_drop_speed
        self.settings.crowd_direction *= -1
    

    def free_memory(self):
        for zombie in self.zombies.copy():
            if zombie.check_bottom():
                self.zombies.remove(zombie)
        
                
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.tank.blittank()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.zombies.draw(self.screen)
        pygame.display.flip()    
        

if __name__ == "__main__":
    zi = Zombie_Invasion()
    zi.run_game()