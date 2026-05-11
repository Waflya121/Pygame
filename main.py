import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Галлага')
clock = pygame.time.Clock()

# Корабль
player = pygame.Rect(375, 520, 40, 25)
speed = 6

running = True
while running:
    # СОБЫТИЯ
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Движение
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= speed
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += speed
    
    # Отрисовка
    screen.fill(BLACK)           # Очищаем экран
    pygame.draw.rect(screen, GREEN, player)  # Рисуем корабль
    pygame.display.flip()        # Показ на экране
    clock.tick(FPS)

pygame.quit()
