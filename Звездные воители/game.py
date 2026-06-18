""" Главный модуль управления игровым процессом (Движок).
Связывает воедино объекты игрока, врагов, снаряды, обрабатывает
физику коллизий и реализует прогрессию сложности волн.
"""

import pygame
import random
import assets
from config import *
from player import Player
from enemy import Enemy
import ui
import vf

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.reset_game()

    def reset_game(self):
        """Сбрасывает все переменные к начальным значениям для перезапуска."""
        self.player = Player()
        self.score = 0
        self.lives = 3
        self.bg_y = 0
        self.bg_speed = 1
        self.wave_count = 0
        self.bg_image = assets.bg_img
        # Динамические списки для отслеживания объектов на экране
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.explosions = []
        self.is_game_over = False
        self.last_attack_time = pygame.time.get_ticks()
        # Хранилище текущего интервала атак (Изменяется с ростом сложности)
        self.attack_interval = BASE_ATTACK_INTERVAL
        # Запускаем фоновую музыку по кругу
        pygame.mixer.music.play(-1)

    def spawn_wave(self):
        """Формирует новую волну противников в виде ровной сетки матрицы."""
        self.enemies.clear()
        self.wave_count += 1
        # Рассчитываем ускоряющийся интервал налетов новой волны
        self.attack_interval = max(MIN_ATTACK_INTERVAL, BASE_ATTACK_INTERVAL - (self.wave_count - 1) * WAVE_DIFFICULTY_STEP)
        
        # Алгоритм распределения врагов по экрану
        side_margin, top_margin = 200, 60
        gap_x = (WIDTH - side_margin * 2) // ENEMY_COLS
        gap_y = 60
        for row in range(ENEMY_ROWS):
            for col in range(ENEMY_COLS):
                # Расчет координат с учетом отступов
                enemy_x = side_margin + col * gap_x + (gap_x // 2 - ENEMY_WIDTH // 2)
                enemy_y = top_margin + row * gap_y
                self.enemies.append(Enemy(enemy_x, enemy_y))

    def check_collisions(self):
        """Выполняет проверку пересечений хитбоксов (Проверка коллизий)."""
        if self.is_game_over: return

        p_rect = self.player.get_rect()

        # Пули игрока
        for e in self.enemies[:]:
            e_rect = e.get_rect()
            for b in self.bullets[:]:
                if e_rect.colliderect(pygame.Rect(b.x, b.y, b.width, b.height)):
                    # Создает эффект взрыва в центре коллизии
                    self.explosions.append(vf.ExplosionCircle(e_rect.centerx, e_rect.centery))
                    
                    # Воспроизведение эффекта взрыва
                    if assets.explosion_snd:
                        assets.explosion_snd.play()

                    if b in self.bullets: self.bullets.remove(b)
                    if e in self.enemies: self.enemies.remove(e)
                    # Начисление очков с бонусом за номер текущей волны
                    self.score += 10 + (self.wave_count - 1) * 10
                    break

        # Пули врагов
        if not self.player.is_invincible:
            for eb in self.enemy_bullets[:]:
                if eb.get_rect().colliderect(p_rect):
                    # Создает эффект взрыва в центре коллизии
                    self.explosions.append(vf.ExplosionCircle(self.player.x + 25, self.player.y + 20, GREEN))
                    
                    # Воспроизведение эффекта взрыва
                    if assets.explosion_snd:
                        assets.explosion_snd.play()
                        
                    self.enemy_bullets.remove(eb)
                    self.lives -= 1
                    self.player.trigger_invincibility()
                    break

        # Таран
        if not self.player.is_invincible:
            for e in self.enemies[:]:
                if e.get_rect().colliderect(p_rect):
                    # Создает эффект взрыва в центре коллизии
                    self.explosions.append(vf.ExplosionCircle(e.x + 20, e.y + 20, RED))
                    
                    # Воспроизведение эффекта взрыва
                    if assets.explosion_snd:
                        assets.explosion_snd.play()
                    
                    self.enemies.remove(e)
                    self.lives -= 1
                    self.player.trigger_invincibility()
                    break
        
        # Проверка условия поражения
        if self.lives <= 0:
            self.is_game_over = True
            pygame.mixer.music.stop() # Отключаем звук при GAME OVER

    def update(self):
        """Обновляет физику и состояния всех объектов."""
        if self.is_game_over:
            return
        
        # Эффект бесконечной прокрутки заднего фона
        self.bg_y += self.bg_speed
        if self.bg_y >= HEIGHT:
            self.bg_y = 0

        self.player.update()
        
        # Обновление частиц и спецэффектов
        for exp in self.explosions[:]:
            exp.update()
            if exp.is_dead: self.explosions.remove(exp)

        self.handle_attacks()
        
        # Обновление позиций врагов и генерация их выстрелов
        for e in self.enemies:
            e.update()
            eb = e.shoot()
            if eb:
                self.enemy_bullets.append(eb)
                # Если враг выстрелил — запускаем звук из ассетов
                if assets.enemy_laser_snd:
                    assets.enemy_laser_snd.play()
        
        # Движение снарядов игрока с очисткой памяти при вылете за экран
        for b in self.bullets[:]:
            b.update()
            if b.y < 0:
                self.bullets.remove(b)
            
        for eb in self.enemy_bullets[:]:
            eb.update()
            if eb.y > HEIGHT:
                self.enemy_bullets.remove(eb)

        # Проверяем столкновения после того, как все объекты обновили свои позиции
        self.check_collisions()

        # Если все враги уничтожены — мгновенно вызываем следующую волну
        if not self.enemies:
            self.spawn_wave()

    def draw(self):
        """Рендерит все игровые объекты на экране компьютера."""
        # Отрисовка двух бесшовных полотен фона для иллюзии полета
        self.screen.blit(self.bg_image, (0, self.bg_y))
        self.screen.blit(self.bg_image, (0, self.bg_y - HEIGHT))
        
        if not self.is_game_over:
            self.player.draw(self.screen)
            for b in self.bullets: b.draw(self.screen)
            for eb in self.enemy_bullets: eb.draw(self.screen)
            for e in self.enemies: e.draw(self.screen)
            for exp in self.explosions: exp.draw(self.screen)
            
            # Рендеринг интерфейса поверх игрового поля
            ui.draw_hud(self.screen, self.lives, self.score, self.wave_count)
        else:
            ui.draw_game_over(self.screen, self.score)

    def handle_attacks(self):
        """Контролирует отправку случайного врага в режим тарана."""
        now = pygame.time.get_ticks()
        if now - self.last_attack_time > self.attack_interval:
            # Выбираем только тех врагов, которые находятся в режиме покоя
            ready = [e for e in self.enemies if not e.is_attacking and not e.is_returning and e.y == e.target_y]
            if ready:
                attacker = random.choice(ready)
                attacker.is_attacking = True
                # Выбираем вектор бокового сдвига
                attacker.current_dive_x = random.randint(-ENEMY_MAX_CHAOS_X, ENEMY_MAX_CHAOS_X)
                self.last_attack_time = now
