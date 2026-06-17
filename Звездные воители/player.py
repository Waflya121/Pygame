import pygame
import assets
from config import *

class Player:
    def __init__(self):
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 70
        self.speed = PLAYER_START_SPEED
        self.image = assets.player_img
        self.is_invincible = False
        self.invincible_timer = 0
        self.invincibility_duration = 3000

    def shoot(self):
        from bullet import Bullet
        return Bullet(self.x + self.width // 2, self.y)

    def trigger_invincibility(self):
        """Включает неуязвимость и запоминает время начала"""
        self.is_invincible = True
        self.invincible_timer = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed

        if self.is_invincible:
            now = pygame.time.get_ticks()
            if now - self.invincible_timer > self.invincibility_duration:
                self.is_invincible = False

    def draw(self, surface):
        if self.is_invincible:
            if (pygame.time.get_ticks() // 100) % 2 == 0:
                return
        
        surface.blit(self.image, (self.x, self.y))
