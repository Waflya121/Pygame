import sys

import pygame

from config import WIDTH, HEIGHT, FPS, TITLE, BLACK
from player import Player

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

player = Player()
bullets = []

# Главный цикл игры
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Проверяем одиночное нажатие на Пробел
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                new_bullet = player.shoot()
                bullets.append(new_bullet)

    player.update()

    for bullet in bullets[:]:
        bullet.update()
        if bullet.y < -bullet.height:
            bullets.remove(bullet)

    screen.fill(BLACK)
    player.draw(screen)

    # Рисуем все пули
    for bullet in bullets:
        bullet.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
