import pygame
import os
from config import WIDTH, HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT

current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, "assets")

player_img = None
enemy_img = None
bg_img = None

def load():
    global player_img, enemy_img, bg_img
    
    # Игрок
    p_file = pygame.image.load(os.path.join(assets_path, "player.png")).convert_alpha()
    player_img = pygame.transform.scale(p_file, (PLAYER_WIDTH, PLAYER_HEIGHT))
    
    # Враги
    e_file = pygame.image.load(os.path.join(assets_path, "enemy.png")).convert_alpha()
    enemy_img = pygame.transform.scale(e_file, (ENEMY_WIDTH, ENEMY_HEIGHT))
    
    # Фон
    b_file = pygame.image.load(os.path.join(assets_path, "background.png")).convert()
    bg_img = pygame.transform.scale(b_file, (WIDTH, HEIGHT))