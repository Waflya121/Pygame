import pygame
import random
from config import *
from player import Player
from enemy import Enemy
import ui
import vf

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.bg_image = pygame.image.load("background.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))
        self.reset_game()

    def reset_game(self):
        self.player = Player()
        self.lives = PLAYER_LIVES
        self.score = 0
        self.bullets = []
        self.enemy_bullets = []
        self.bg_y = 0
        self.bg_speed = 1
        self.enemies = []
        self.explosions = []
        self.wave_count = 0
        self.is_game_over = False
        self.last_attack_time = pygame.time.get_ticks()

    def spawn_wave(self):
        self.enemies.clear()
        self.wave_count += 1
        self.attack_interval = max(MIN_ATTACK_INTERVAL, BASE_ATTACK_INTERVAL - (self.wave_count - 1) * WAVE_DIFFICULTY_STEP)
        
        side_margin, top_margin = 200, 60
        gap_x = (WIDTH - side_margin * 2) // ENEMY_COLS
        gap_y = 60
        for row in range(ENEMY_ROWS):
            for col in range(ENEMY_COLS):
                enemy_x = side_margin + col * gap_x + (gap_x // 2 - ENEMY_WIDTH // 2)
                enemy_y = top_margin + row * gap_y
                self.enemies.append(Enemy(enemy_x, enemy_y))

    def check_collisions(self):
        if self.is_game_over: return

        p_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)

        # Пули игрока
        for e in self.enemies[:]:
            e_rect = e.get_rect()
            for b in self.bullets[:]:
                if e_rect.colliderect(pygame.Rect(b.x, b.y, b.width, b.height)):
                    self.explosions.append(vf.ExplosionCircle(e.x + 20, e.y + 20)) # Взрыв врага
                    if b in self.bullets: self.bullets.remove(b)
                    if e in self.enemies: self.enemies.remove(e)
                    self.score += 10 + (self.wave_count - 1) * 10
                    break

        # Пули врагов
        if not self.player.is_invincible:
            for eb in self.enemy_bullets[:]:
                if eb.get_rect().colliderect(p_rect):
                    self.explosions.append(vf.ExplosionCircle(self.player.x + 25, self.player.y + 20, (0, 255, 0)))
                    self.enemy_bullets.remove(eb)
                    self.lives -= 1
                    self.player.trigger_invincibility()
                    break

        # Таран
        if not self.player.is_invincible:
            for e in self.enemies[:]:
                if e.get_rect().colliderect(p_rect):
                    self.explosions.append(vf.ExplosionCircle(e.x + 20, e.y + 20, (255, 0, 0)))
                    self.enemies.remove(e)
                    self.lives -= 1
                    self.player.trigger_invincibility()
                    break

        if self.lives <= 0:
            self.is_game_over = True

    def update(self):
        if self.is_game_over: return
        
        self.bg_y += self.bg_speed
        if self.bg_y >= HEIGHT:
            self.bg_y = 0

        self.player.update()
        
        for exp in self.explosions[:]:
            exp.update()
            if exp.is_dead: self.explosions.remove(exp)

        self.handle_attacks()
        self.check_collisions()
        
        for e in self.enemies:
            eb = e.shoot()
            if eb: self.enemy_bullets.append(eb)
        
        for b in self.bullets[:]:
            b.update()
            if b.y < 0: self.bullets.remove(b)
            
        for eb in self.enemy_bullets[:]:
            eb.update()
            if eb.y > HEIGHT: self.enemy_bullets.remove(eb)
            
        for e in self.enemies:
            e.update()

        if not self.enemies:
            self.spawn_wave()

    def draw(self):
        self.screen.blit(self.bg_image, (0, self.bg_y))
        self.screen.blit(self.bg_image, (0, self.bg_y - HEIGHT))
        
        if not self.is_game_over:
            self.player.draw(self.screen)
            for b in self.bullets: b.draw(self.screen)
            for eb in self.enemy_bullets: eb.draw(self.screen)
            for e in self.enemies: e.draw(self.screen)
            for exp in self.explosions: exp.draw(self.screen)
            
            ui.draw_hud(self.screen, self.lives, self.score, self.wave_count)
        else:
            ui.draw_game_over(self.screen, self.score)

    def handle_attacks(self):
        now = pygame.time.get_ticks()
        if now - self.last_attack_time > self.attack_interval:
            ready = [e for e in self.enemies if not e.is_attacking and not e.is_returning and e.y == e.target_y]
            if ready:
                attacker = random.choice(ready)
                attacker.is_attacking = True
                attacker.current_dive_x = random.randint(-ENEMY_MAX_CHAOS_X, ENEMY_MAX_CHAOS_X)
                self.last_attack_time = now
