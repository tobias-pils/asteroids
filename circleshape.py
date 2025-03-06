import pygame
from constants import SCREEN_WIDTH
from constants import SCREEN_HEIGHT

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(getattr(self, "containers"))
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    def is_colliding(self, other):
        distance = self.position.distance_to(other.position)
        return distance <= self.radius + other.radius

    def wrap(self, margin=0):
        if self.position.x + self.radius + margin < 0:
            self.position.x = self.radius + SCREEN_WIDTH + margin
        if self.position.x - self.radius - margin > SCREEN_WIDTH:
            self.position.x = -self.radius - margin
        if self.position.y + self.radius + margin < 0:
            self.position.y = self.radius + SCREEN_HEIGHT + margin
        if self.position.y - self.radius - margin > SCREEN_HEIGHT:
            self.position.y = -self.radius - margin
