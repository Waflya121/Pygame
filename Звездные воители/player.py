""" Модуль логики и отрисовки игрока.
Описывает физику перемещения корабля пользователя, систему его
неуязвимости после урона и анимацию визуального мерцания.
"""

import pygame
import assets
from bullet import Bullet
from config import *

class Player:
    def __init__(self):
        """Инициализирует базовые параметры игрока."""
        self.image = assets.player_img
        self.rect = self.image.get_rect()
        # Размещает игрока строго по центру нижней части экрана
        self.x = WIDTH // 2 - self.rect.width // 2
        self.y = HEIGHT - 70
        self.speed = PLAYER_START_SPEED
        
        # Параметры системы неуязвимости при получении урона
        self.is_invincible = False
        self.invincible_timer = 0
        self.invincibility_duration = 3000 # Длительность щита

    def shoot(self):
        return Bullet(self.x + self.rect.width // 2, self.y)

    def trigger_invincibility(self):
        """Включает неуязвимость и запоминает время начала"""
        self.is_invincible = True
        self.invincible_timer = pygame.time.get_ticks()

    def update(self):
        """Обновляет состояние игрока и проверяет таймер щита."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.rect.width:
            self.x += self.speed

        # Проверка истечения таймера действия защитного экрана
        if self.is_invincible:
            now = pygame.time.get_ticks()
            if now - self.invincible_timer > self.invincibility_duration:
                self.is_invincible = False

    def draw(self, surface):
        """Отрисовывка игрока с эффектом мигания, если он неуязвим."""
        if self.is_invincible:
            # Рисуем спрайт только каждый 4-й кадр(эффект мигания)
            if (pygame.time.get_ticks() // 100) % 2 == 0:
                return

        surface.blit(self.image, (self.x, self.y))
    
    def get_rect(self):
        """Возвращает актуальный хитбокс игрока."""
        self.rect.topleft = (self.x, self.y)
        return self.rect
