import pygame
import random

from constants import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    COLLECTIBLE_SHIELD_LIFETIME
)

class Shield(pygame.sprite.Sprite):
    WIDTH = 20
    HEIGHT = 25

    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(getattr(self, "containers"))
        else:
            super().__init__()

        self.width = Shield.WIDTH
        self.height = Shield.HEIGHT
        self.init_x = self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.init_y = self.y = random.randint(0, SCREEN_HEIGHT)
        self.resize_ms = 0
        self.lifetime = COLLECTIBLE_SHIELD_LIFETIME

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
        self.width = Shield.WIDTH + resize
        self.height = Shield.HEIGHT + resize

    def points(self):
        return [
            (self.x, self.y), # top_left
            (self.x + self.width, self.y), # top_right
            (self.x + self.width, self.y + self.width), # bottom_right
            (self.x + self.width / 2, self.y + self.height), # bottom_middle
            (self.x, self.y + self.width) # bottom_left
        ]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.points(), 2)

    def is_point_inside(self, point):
        # point is to the left, above or to the right
        if (
            self.x > point.x
            or self.y > point.y
            or self.x + self.width < point.x
        ):
            return False

        # point is in rectangle
        if self.y + self.width >= point.y:
            return True

        # TODO: collision with triangular tip

        return False

    def apply_to_player(self, player):
        if player.is_shielded:
            return False

        player.is_shielded = True
        return True
