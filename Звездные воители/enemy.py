import pygame
from config import HEIGHT, ENEMY_SPEED, RED, ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_RETURN_SPEED, ENEMY_SHOOT_CHANCE
from bullet import EnemyBullet

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
        self.return_speed = ENEMY_RETURN_SPEED
        self.is_attacking = False
        self.is_returning = False
        self.color = RED

    def shoot(self):
        if self.is_attacking and random.randint(0, ENEMY_SHOOT_CHANCE) == 1:
            return EnemyBullet(self.x + self.width // 2, self.y + self.height)
        return None

    def update(self):
        if self.is_attacking:
            self.y += self.speed
            self.x += self.current_dive_x
            if self.y > HEIGHT:
                self.y = -self.height
                self.is_attacking = False
                self.is_returning = True

        elif self.is_returning:
            if self.y < 0:
                if abs(self.x - self.original_x) > 3:
                    if self.x < self.original_x: self.x += 6 
                    else: self.x -= 6
                else:
                    self.x = self.original_x
                    self.y += self.return_speed
            else:
                self.y += self.return_speed
            
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
