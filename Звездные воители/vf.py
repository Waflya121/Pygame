""" Модуль визуальных эффектов (Visual Effects).
Реализует анимацию взрывов на базе геометрических форм.
"""
import pygame

class ExplosionCircle:
    def __init__(self, x, y, color=(255, 165, 0)):
        """Устанавливает стартовые координаты и параметры взрыва."""
        self.x = x
        self.y = y
        self.radius = 5
        self.max_radius = 30
        self.color = color
        self.is_dead = False

    def update(self):
        self.radius += 2
        # Если радиус превысил лимит — убираем объект
        if self.radius > self.max_radius:
            self.is_dead = True

    def draw(self, surface):
        """Рисует контур окружности на экране, если еще такое возможно."""
        if not self.is_dead:
            pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius, 2)
