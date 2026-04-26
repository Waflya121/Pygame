import pygame

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 640, 480
FPS = 60

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Галлага')
clock = pygame.time.Clock()

running = True

while running:
    pygame.event.get()
    screen.fill(BLACK)
    pygame.display.flip()
    clock.tick(FPS)
