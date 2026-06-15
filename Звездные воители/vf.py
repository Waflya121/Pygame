import pygame

class ExplosionCircle:
    def __init__(self, x, y, color=(255, 165, 0)):
        self.x = x
        self.y = y
        self.radius = 5
        self.max_radius = 30
        self.color = color
        self.is_dead = False

    def update(self):
        self.radius += 2
        if self.radius > self.max_radius:
            self.is_dead = True

    def draw(self, surface):
        if not self.is_dead:
            pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius, 2)