""" Главный модуль игры.
Инициализирует подсистемы Pygame, создает игровые менеджеры, запускает
основной цикл обработки событий и контролирует смену экранов.
"""

import sys
import pygame
import assets
from config import WIDTH, HEIGHT, FPS, TITLE
from game import Game
from menu import Menu

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    assets.load() # Единоразовая загрузка графики при старте

    # Создание ключевых контроллеров
    game = Game(screen)
    menu = Menu(screen)

    # Изначальное состояние (Главное меню)
    state = "MENU"
    running = True
    
    # Главный цикл
    while running:
        # Стабилизация кадровой частоты
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if state == "MENU":
                res = menu.handle_events(event)
                if res == "GAME":
                    state = "GAME"
                    game.reset_game() # Полный сброс параметров перед стартом новой игры
                elif res == "EXIT":
                    running = False
                
            elif state == "GAME":
                if event.type == pygame.KEYDOWN:
                    # Выстрел игрока по нажатию на пробел
                    if event.key == pygame.K_SPACE and not game.is_game_over:
                        game.bullets.append(game.player.shoot())
                    # Перезапуск матча на клавишу R в случае Game Over
                    if event.key == pygame.K_r and game.is_game_over:
                        game.reset_game()
                    # Возврат в главное меню по кнопке ESC
                    if event.key == pygame.K_ESCAPE:
                        state = "MENU"
        
        if state == "MENU":
            menu.draw()
        elif state == "GAME":
            game.update()
            game.draw()
            
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
