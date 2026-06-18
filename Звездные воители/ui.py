""" Модуль графического интерфейса пользователя (User Interface).
Отвечает за отрисовку HUD (очки, жизни, волны) во время матча, а также
статических экранов проигрыша. Не содержит внутренней логики игры.
"""
import pygame
from config import WIDTH, HEIGHT, WHITE, RED, GREEN, YELLOW

pygame.font.init()
font_main = pygame.font.SysFont("Arial", 24)
font_big = pygame.font.SysFont("Arial", 64)

def draw_hud(screen, lives, score, wave):
    """Рисует жизни, очки и номер волны"""
    l_text = font_main.render(f"Lives: {lives}", True, WHITE)
    s_text = font_main.render(f"Score: {score}", True, WHITE)
    w_text = font_main.render(f"Wave: {wave}", True, YELLOW)
    
    screen.blit(l_text, (20, 20))
    screen.blit(s_text, (WIDTH - s_text.get_width() - 20, 20))
    screen.blit(w_text, (WIDTH // 2 - w_text.get_width() // 2, 20))

def draw_game_over(screen, score):
    """Рисует экран окончания игры"""
    txt = font_big.render("GAME OVER", True, RED)
    screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - 80))
    
    score_txt = font_main.render(f"Final Score: {score}", True, WHITE)
    screen.blit(score_txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 + 10))
    
    retry_txt = font_main.render("Press R to Restart", True, GREEN)
    screen.blit(retry_txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 + 50))
