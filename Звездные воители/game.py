# game.py
import pygame
import random
from config import (
    WIDTH, HEIGHT, BLACK, ENEMY_COUNT_IN_WAVE, ENEMY_WIDTH,
    BASE_ATTACK_INTERVAL, MIN_ATTACK_INTERVAL, WAVE_DIFFICULTY_STEP,
    ENEMY_MAX_CHAOS_X
)
from player import Player
from enemy import Enemy

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player()
        self.bullets = []
        self.enemies = []
        self.wave_count = 0
        self.attack_interval = BASE_ATTACK_INTERVAL
        self.last_attack_time = pygame.time.get_ticks()

    def spawn_wave(self):
        self.wave_count += 1
        new_interval = BASE_ATTACK_INTERVAL - (self.wave_count - 1) * WAVE_DIFFICULTY_STEP
        self.attack_interval = max(MIN_ATTACK_INTERVAL, new_interval)
        
        side_margin = 150
        available_width = WIDTH - (side_margin * 2) - ENEMY_WIDTH
        step_x = available_width / (ENEMY_COUNT_IN_WAVE - 1)

        for i in range(ENEMY_COUNT_IN_WAVE):
            enemy_x = side_margin + int(i * step_x)
            self.enemies.append(Enemy(enemy_x, 100))

    def handle_attacks(self):
        now = pygame.time.get_ticks()
        if now - self.last_attack_time > self.attack_interval:
            ready_enemies = [
                e for e in self.enemies 
                if not e.is_attacking and not e.is_returning and e.y == e.target_y
            ]
            
            if ready_enemies:
                attacker = random.choice(ready_enemies)
                attacker.is_attacking = True
                attacker.current_dive_x = random.randint(-ENEMY_MAX_CHAOS_X, ENEMY_MAX_CHAOS_X)
                self.last_attack_time = now

    def check_collisions(self):
        for e in self.enemies[:]:
            e_rect = e.get_rect()
            for b in self.bullets[:]:
                b_rect = pygame.Rect(b.x, b.y, b.width, b.height)
                if e_rect.colliderect(b_rect):
                    if b in self.bullets: self.bullets.remove(b)
                    if e in self.enemies: self.enemies.remove(e)
                    break

    def update(self):
        self.player.update()
        self.handle_attacks()
        self.check_collisions()

        for b in self.bullets[:]:
            b.update()
            if b.y < 0: self.bullets.remove(b)

        for e in self.enemies:
            e.update()

        if not self.enemies:
            self.spawn_wave()

    def draw(self):
        self.screen.fill(BLACK)
        self.player.draw(self.screen)
        for b in self.bullets: b.draw(self.screen)
        for e in self.enemies: e.draw(self.screen)