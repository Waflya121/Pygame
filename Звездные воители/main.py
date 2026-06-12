import sys

import pygame

from config import WIDTH, HEIGHT, FPS, TITLE, BLACK
from player import Player

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

player = Player()

# Главный цикл игры
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update()

    screen.fill(BLACK)
    player.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()