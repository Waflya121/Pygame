""" Модуль конфигурации игры.
Содержит все глобальные константы, настройки экрана, скоростей,
цветовых палитр и параметров баланса сложности.
"""

# Экран
WIDTH = 1000
HEIGHT = 700
FPS = 60
TITLE = "Звездные воители"

# Звук
SOUND_VOLUME = 0.1
MUSIC_VOLUME = 0.3
ENEMY_SOUND_VOLUME = 0.1

# Цвета (RGB)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Игрок
PLAYER_START_SPEED = 5
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 80
PLAYER_LIVES = 3

# Пули
BULLET_SPEED = 7
ENEMY_BULLET_SPEED = 4
ENEMY_SHOOT_CHANCE = 50

# Враги
ENEMY_ROWS = 3
ENEMY_COLS = 6
ENEMY_WIDTH = 80
ENEMY_HEIGHT = 80
ENEMY_SPEED = 4
ENEMY_RETURN_SPEED = 10
ENEMY_MAX_CHAOS_X = 3

# Прогрессия сложности
BASE_ATTACK_INTERVAL = 1200
MIN_ATTACK_INTERVAL = 300
WAVE_DIFFICULTY_STEP = 150
