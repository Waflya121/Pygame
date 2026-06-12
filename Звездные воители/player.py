import pygame

from config import WIDTH, HEIGHT, GREEN, PLAYER_START_SPEED, PLAYER_WIDTH, PLAYER_HEIGHT


class Player:
    def __init__(self):
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 20
        self.speed = PLAYER_START_SPEED
        self.color = GREEN

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        # Ограничение движения границами экрана
        if self.x < 0:
            self.x = 0
        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width

        if self.y < 0:
            self.y = 0
        if self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height

    def draw(self, surface):
        pygame.draw.rect(
            surface, self.color, (self.x, self.y, self.width, self.height)
        )