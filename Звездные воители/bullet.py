"""Модуль описания боевых снарядов (Пуль).
Содержит классы для лазеров игрока и вражеских кораблей.
"""

import pygame
from config import YELLOW, RED, BULLET_SPEED, ENEMY_BULLET_SPEED

class Bullet:
    def __init__(self, x, y):
        """Инициализирует пулю игрока в указанных координатах."""
        self.width = 5
        self.height = 15
        # Центрируем пулю относительно дула корабля
        self.x = x - self.width // 2
        self.y = y
        self.speed = BULLET_SPEED
        self.color = YELLOW

    def update(self):
        """Перемещает пулю вверх по вертикали."""
        self.y -= self.speed

    def draw(self, surface):
        """Отрисовывает пулю в виде прямоугольника на заданной поверхности."""
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

class EnemyBullet:
    def __init__(self, x, y):
        """Инициализирует вражескую пулю."""
        self.width = 5
        self.height = 15
        # Также центрирует пулю относительно дула корабля противника
        self.x = x - self.width // 2
        self.y = y
        self.speed = ENEMY_BULLET_SPEED
        self.color = RED

    def update(self):
        """Перемещает пулю вниз по вертикали."""
        self.y += self.speed

    def draw(self, surface):
        """Отрисовка вражеской пули."""
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        
    def get_rect(self):
        """Возвращает объект pygame.Rect для детекции коллизий."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
