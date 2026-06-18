""" Модуль отрисовки главного меню игры.
Предоставляет графический интерфейс с кнопками запуска и выхода,
реализует визуальный отклик при наведении курсора мыши.
"""

import pygame
import assets
from config import WIDTH, HEIGHT

class Menu:
    def __init__(self, screen):
        """Создает зоны кнопок и настраивает шрифты интерфейса."""
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 50, bold=True)
        
        # Позиционирование кнопок по центру экрана
        self.start_rect = pygame.Rect(WIDTH // 2 - 100, 300, 200, 60)
        self.exit_rect = pygame.Rect(WIDTH // 2 - 100, 400, 200, 60)
        
        # Цвет кнопок (обычное состояние и при наведении)
        self.color_normal = (0, 200, 255)
        self.color_hover = (222, 255, 154)

    def draw(self):
        """Отрисовывает элементы меню и проверяет наведение курсора."""
        # Задний фон
        self.screen.blit(assets.bg_img, (0, 0))
        
        # Заголовок
        title = self.font.render("STAR WARRIORS", True, (255, 255, 255))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))
        
        # Координаты мышки
        mouse_pos = pygame.mouse.get_pos()
        
        # Кнопка START
        start_color = self.color_hover if self.start_rect.collidepoint(mouse_pos) else self.color_normal
        pygame.draw.rect(self.screen, start_color, self.start_rect, 2, border_radius=10)
        start_txt = self.font.render("START", True, start_color)
        self.screen.blit(start_txt, (self.start_rect.centerx - start_txt.get_width() // 2, self.start_rect.centery - 25))
        
        # Кнопка EXIT
        exit_color = self.color_hover if self.exit_rect.collidepoint(mouse_pos) else self.color_normal
        pygame.draw.rect(self.screen, exit_color, self.exit_rect, 2, border_radius=10)
        exit_txt = self.font.render("EXIT", True, exit_color)
        self.screen.blit(exit_txt, (self.exit_rect.centerx - exit_txt.get_width() // 2, self.exit_rect.centery - 25))

    def handle_events(self, event):
        """Возвращает новое состояние игры или None"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Проверка нажатия левой кнопки мыши
                if self.start_rect.collidepoint(event.pos):
                    return "GAME"
                if self.exit_rect.collidepoint(event.pos):
                    return "EXIT"
        return None