import pygame
from circleshape import CircleShape

class Blast(CircleShape):
    def __init__(self, x, y, blast_radius):
        super().__init__(x, y, 0)
        self.end_radius = blast_radius

    def update(self, dt):
        if self.radius >= self.end_radius:
            self.kill()

        self.radius += self.end_radius * dt
        if self.radius > self.end_radius:
            self.radius = self.end_radius

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)
        pygame.draw.circle(screen, "white", self.position, self.radius * 0.9, 1)
        pygame.draw.circle(screen, "white", self.position, self.radius * 0.7, 1)
