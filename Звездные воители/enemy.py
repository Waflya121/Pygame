# enemy.py
import pygame
from config import HEIGHT, ENEMY_SPEED, RED, ENEMY_WIDTH, ENEMY_HEIGHT

class Enemy:
    def __init__(self, start_x, target_y):
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.original_x = start_x
        self.x = start_x
        self.y = -self.height
        self.target_y = target_y
        
        self.current_dive_x = 0
        self.speed = ENEMY_SPEED
        self.is_attacking = False
        self.is_returning = False
        self.color = RED

    def update(self):
        if self.is_attacking:
            self.y += self.speed
            self.x += self.current_dive_x
            
            if self.y > HEIGHT:
                self.y = -self.height
                self.is_attacking = False
                self.is_returning = True

        elif self.is_returning:
            if abs(self.x - self.original_x) > 2:
                if self.x < self.original_x: self.x += 3
                else: self.x -= 3
            else:
                self.x = self.original_x
                self.y += self.speed
            
            if self.y >= self.target_y:
                self.y = self.target_y
                self.is_returning = False

        else:
            if self.y < self.target_y:
                self.y = min(self.y + self.speed, self.target_y)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)