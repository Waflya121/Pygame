import pygame
from config import YELLOW, RED, BULLET_SPEED, ENEMY_BULLET_SPEED

class Bullet:
    def __init__(self, x, y):
        self.width = 5
        self.height = 15
        self.x = x - self.width // 2
        self.y = y
        self.speed = BULLET_SPEED
        self.color = YELLOW

    def update(self):
        self.y -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

class EnemyBullet:
    def __init__(self, x, y):
        self.width = 5
        self.height = 15
        self.x = x - self.width // 2
        self.y = y
        self.speed = ENEMY_BULLET_SPEED
        self.color = RED

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
