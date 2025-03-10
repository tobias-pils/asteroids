import pygame
import random

from constants import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    COLLECTIBLE_SPEED_LIFETIME,
    SPEED_EFFECT_DURATION
)

class Speed(pygame.sprite.Sprite):
    WIDTH = 20
    HEIGHT = 25

    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(getattr(self, "containers"))
        else:
            super().__init__()

        self.width = Speed.WIDTH
        self.height = Speed.HEIGHT
        self.init_x = self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.init_y = self.y = random.randint(0, SCREEN_HEIGHT)
        self.resize_ms = 0
        self.lifetime = COLLECTIBLE_SPEED_LIFETIME

    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime < 0:
            self.kill()

        self.resize_ms += dt * 1000
        ms_per_phase = 50
        num_phases = 20
        cycle_length = ms_per_phase * num_phases
        resize_progress = abs(self.resize_ms % cycle_length - cycle_length / 2)
        resize = resize_progress // ms_per_phase

        self.x = self.init_x - resize / 2
        self.y = self.init_y - resize / 2
        self.width = Speed.WIDTH + resize
        self.height = Speed.HEIGHT + resize

    def points(self):
        return [
            (self.x, self.y), # top_left
            (self.x + self.width, self.y), # top_right
            (self.x + self.width, self.y + self.height), # bottom_right
            (self.x, self.y + self.height) # bottom_left
        ]

    def draw(self, screen):
        pygame.draw.line(screen, "white", (self.x, self.y + self.height / 3), (self.x + self.width / 2, self.y))
        pygame.draw.line(screen, "white", (self.x + self.width / 2, self.y), (self.x + self.width, self.y + self.height / 3))

        pygame.draw.line(screen, "white", (self.x, self.y + self.height / 1.5), (self.x + self.width / 2, self.y + self.height / 3))
        pygame.draw.line(screen, "white", (self.x + self.width / 2, self.y + self.height / 3), (self.x + self.width, self.y + self.height / 1.5))

        pygame.draw.line(screen, "white", (self.x, self.y + self.height), (self.x + self.width / 2, self.y + self.height / 1.5))
        pygame.draw.line(screen, "white", (self.x + self.width / 2, self.y + self.height / 1.5), (self.x + self.width, self.y + self.height))

    def is_point_inside(self, point):
        return (
            self.x <= point.x and
            self.x + self.width >= point.x and
            self.y <= point.y and
            self.y + self.height >= point.y
        )

    def apply_to_player(self, player):
        if player.boosted_time > 0:
            return False

        player.boosted_time = SPEED_EFFECT_DURATION
        return True
