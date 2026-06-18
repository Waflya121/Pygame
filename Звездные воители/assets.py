""" Модуль управления графическими ресурсами (Assets Manager).
Отвечает за безопасную загрузку, масштабирование и оптимизацию спрайтов.
"""

import pygame
import os
from config import WIDTH, HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT, SOUND_VOLUME, ENEMY_SOUND_VOLUME

# Определение путей к файлам
current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, "assets")

# Глобальные переменные-контейнеры для хранения поверхностей
player_img = None
enemy_img = None
bg_img = None

# Глобальные переменные-контейнеры для хранения звуков
laser_snd = None
enemy_laser_snd = None
explosion_snd = None

def load():
    """Загружает графические файлы из папки assets в оперативную память.

    Применяет методы .convert() для ускорения рендеринга видеокартой.
    """
    global player_img, enemy_img, bg_img
    global laser_snd, enemy_laser_snd, explosion_snd
    
    # Игрок
    p_file = pygame.image.load(os.path.join(assets_path, "player.png")).convert_alpha()
    player_img = pygame.transform.scale(p_file, (PLAYER_WIDTH, PLAYER_HEIGHT))
    
    # Враги
    e_file = pygame.image.load(os.path.join(assets_path, "enemy.png")).convert_alpha()
    enemy_img = pygame.transform.scale(e_file, (ENEMY_WIDTH, ENEMY_HEIGHT))
    
    # Фон
    b_file = pygame.image.load(os.path.join(assets_path, "background.png")).convert()
    bg_img = pygame.transform.scale(b_file, (WIDTH, HEIGHT))
    
    # Фоновая музыка
    pygame.mixer.music.load(os.path.join(assets_path, "background.mp3"))
    pygame.mixer.music.set_volume(0.3)
    
    # Короткие эффекты
    laser_snd = pygame.mixer.Sound(os.path.join(assets_path, "laser.mp3"))
    enemy_laser_snd = pygame.mixer.Sound(os.path.join(assets_path, "enemy_laser.wav"))
    explosion_snd = pygame.mixer.Sound(os.path.join(assets_path, "explosion.mp3"))
    
    # Настройка громкости из конфига
    laser_snd.set_volume(SOUND_VOLUME)
    enemy_laser_snd.set_volume(ENEMY_SOUND_VOLUME)
    explosion_snd.set_volume(SOUND_VOLUME)
