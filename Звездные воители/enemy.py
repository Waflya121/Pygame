""" Модуль логики поведения вражеских кораблей (ИИ пришельцев).
Реализует конечный автомат противника: плавное появление, нахождение в сетке,
тактическое пикирование (камикадзе-дайвинг) на игрока и возврат на позицию.
"""

import pygame
import random
import assets
from config import HEIGHT, ENEMY_SPEED, ENEMY_RETURN_SPEED, RED, ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_SHOOT_CHANCE
from bullet import EnemyBullet

class Enemy:
    def __init__(self, start_x, target_y):
        """Инициализирует начальные и целевые координаты врага."""
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        # Фиксация исходной точки в эскадрилье
        self.original_x = start_x
        self.x = start_x
        # Спавн за верхней границей экрана для эффекта влета в игру
        self.y = -self.height
        self.target_y = target_y
        self.image = assets.enemy_img
        self.current_dive_x = 0
        self.speed = ENEMY_SPEED
        self.return_speed = ENEMY_RETURN_SPEED
        self.is_attacking = False
        self.is_returning = False
        self.color = RED

    def shoot(self):
        """ Генерирует выстрел лазером с определенной долей вероятности 1/50.
        Враги могут стрелять только тогда, когда находятся в фазе активной атаки.
        """
        if self.is_attacking and random.randint(0, ENEMY_SHOOT_CHANCE) == 1:
            return EnemyBullet(self.x + self.width // 2, self.y + self.height)
        return None

    def update(self):
        # Состояние 1: Активное пикирование вниз (атака)
        if self.is_attacking:
            self.y += self.speed
            self.x += self.current_dive_x
            # Если улетел за нижний край экрана — отправляем на возврат сверху
            if self.y > HEIGHT:
                self.y = -self.height
                self.is_attacking = False
                self.is_returning = True

        # Состояние 2: Возвращение на свою позицию в сетке волны
        elif self.is_returning:
            if self.y < 0:
                # Находясь за экраном, корректируем координату X к исходной
                if abs(self.x - self.original_x) > 3:
                    if self.x < self.original_x: self.x += 6 
                    else: self.x -= 6
                else:
                    self.x = self.original_x
                    self.y += self.return_speed
            else:
                self.y += self.return_speed
            
            # Когда долетел до исходной строки — фиксируем врага в режиме покоя
            if self.y >= self.target_y:
                self.y = self.target_y
                self.is_returning = False

        # Состояние 3: Спокойный стартовый влет сверху при спавне новой волны
        else:
            if self.y < self.target_y:
                self.y = min(self.y + self.speed, self.target_y)

    def draw(self, surface):
        """Отрисовка вражеского корабля."""
        surface.blit(self.image, (self.x, self.y))

    def get_rect(self):
        """Возвращает коллизию врага."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
