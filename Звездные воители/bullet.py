import pygame

from config import BULLET_SPEED, BULLET_WIDTH, BULLET_HEIGHT, YELLOW


class Bullet:
    def __init__(self, x, y):
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        # Позиционируем пулю по центру корабля
        self.x = x - self.width // 2
        self.y = y
        self.speed = BULLET_SPEED
        self.color = YELLOW

    def update(self):
        # Пуля летит вверх
        self.y -= self.speed

    def draw(self, surface):
        pygame.draw.rect(
            surface, self.color, (self.x, self.y, self.width, self.height)
        )