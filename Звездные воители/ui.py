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
    screen.blit(s_text, (WIDTH - 180, 20))
    screen.blit(w_text, (WIDTH // 2 - 40, 20))

def draw_game_over(screen, score):
    """Рисует экран окончания игры"""
    txt = font_big.render("GAME OVER", True, RED)
    screen.blit(txt, (WIDTH // 2 - 160, HEIGHT // 2 - 50))
    
    score_txt = font_main.render(f"Final Score: {score}", True, WHITE)
    screen.blit(score_txt, (WIDTH // 2 - 70, HEIGHT // 2 + 30))
    
    retry_txt = font_main.render("Press R to Restart", True, GREEN)
    screen.blit(retry_txt, (WIDTH // 2 - 90, HEIGHT // 2 + 70))