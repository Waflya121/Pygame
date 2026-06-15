import pygame
import random
import sys
from config import *
from player import Player
from enemy import Enemy

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player()
        self.lives = PLAYER_LIVES
        self.score = 0
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.wave_count = 0
        self.attack_interval = BASE_ATTACK_INTERVAL
        self.last_attack_time = pygame.time.get_ticks()
        self.font = pygame.font.SysFont("Arial", 24)

    def spawn_wave(self):
        self.wave_count += 1
        self.current_points = POINTS_PER_ENEMY + (self.wave_count - 1) * 20
        
        new_interval = BASE_ATTACK_INTERVAL - (self.wave_count - 1) * WAVE_DIFFICULTY_STEP
        self.attack_interval = max(MIN_ATTACK_INTERVAL, new_interval)
        side_margin = 150
        available_w = WIDTH - (side_margin * 2) - ENEMY_WIDTH
        step_x = available_w / (ENEMY_COUNT_IN_WAVE - 1)
        for i in range(ENEMY_COUNT_IN_WAVE):
            self.enemies.append(Enemy(side_margin + int(i * step_x), 100))

    def handle_attacks(self):
        now = pygame.time.get_ticks()
        if now - self.last_attack_time > self.attack_interval:
            ready = [e for e in self.enemies if not e.is_attacking and not e.is_returning and e.y == e.target_y]
            if ready:
                attacker = random.choice(ready)
                attacker.is_attacking = True
                attacker.current_dive_x = random.randint(-ENEMY_MAX_CHAOS_X, ENEMY_MAX_CHAOS_X)
                self.last_attack_time = now

    def check_collisions(self):
        # Попадание игрока
        for e in self.enemies[:]:
            e_rect = e.get_rect()
            for b in self.bullets[:]:
                b_rect = pygame.Rect(b.x, b.y, b.width, b.height)
                if e_rect.colliderect(b_rect):
                    if b in self.bullets: self.bullets.remove(b)
                    if e in self.enemies: self.enemies.remove(e)
                    self.score += self.current_points # НАЧИСЛЯЕМ ОЧКИ
                    break

        # Попадание врага
        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
        for eb in self.enemy_bullets[:]:
            eb_rect = pygame.Rect(eb.x, eb.y, eb.width, eb.height)
            if eb_rect.colliderect(player_rect):
                self.enemy_bullets.remove(eb)
                self.lives -= 1
                if self.lives <= 0: self.game_over()

        # Таран
        for e in self.enemies[:]:
            if e.get_rect().colliderect(player_rect):
                self.enemies.remove(e)
                self.lives -= 1
                if self.lives <= 0: self.game_over()

    def game_over(self):
        print("GAME OVER")
        pygame.quit()
        sys.exit()

    def update(self):
        self.player.update()
        self.handle_attacks()
        self.check_collisions()

        # Стрельба врагов
        for e in self.enemies:
            eb = e.shoot()
            if eb: self.enemy_bullets.append(eb)

        # Пули игрока
        for b in self.bullets[:]:
            b.update()
            if b.y < 0: self.bullets.remove(b)

        # Пули врага
        for eb in self.enemy_bullets[:]:
            eb.update()
            if eb.y > HEIGHT: self.enemy_bullets.remove(eb)

        for e in self.enemies:
            e.update()

        if not self.enemies:
            self.spawn_wave()

    def draw(self):
        self.screen.fill(BLACK)
        self.player.draw(self.screen)
        for b in self.bullets: b.draw(self.screen)
        for eb in self.enemy_bullets: eb.draw(self.screen)
        for e in self.enemies: e.draw(self.screen)
        
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        wave_text = self.font.render(f"Wave: {self.wave_count}", True, YELLOW)
        
        self.screen.blit(lives_text, (10, 10))
        self.screen.blit(score_text, (WIDTH - 150, 10))
        self.screen.blit(wave_text, (WIDTH // 2 - 40, 10))
