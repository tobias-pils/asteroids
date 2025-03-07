import pygame
import random
import math
from constants import (
    ASTEROID_MIN_RADIUS,
    ASTEROID_SCORE_FACTOR,
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(getattr(self, "containers"))
        else:
            super().__init__()

        self.radius = radius
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)

        # create left circle
        self.left_radius = radius + random.randrange(2, 10)
        self.left_position = pygame.Vector2(-1, 0).rotate(random.randrange(-60, 60))
        self.left_position.scale_to_length(random.randrange(1, radius))

        # create right circle
        self.right_radius = radius + random.randrange(2, 10)
        self.right_position = pygame.Vector2(1, 0).rotate(random.randrange(-60, 60))
        self.right_position.scale_to_length(random.randrange(1, radius))

        # find angles for drawing arcs
        dist_sqr = self.left_position.distance_squared_to(self.right_position)
        dist = dist_sqr ** 0.5
        l = (self.left_radius ** 2 - self.right_radius ** 2 + dist_sqr) / (2 * dist)

        left_absolute_position = self.position + self.left_position
        right_absolute_position = self.position + self.right_position
        rel_angle = math.acos((right_absolute_position.x - left_absolute_position.x) / dist)
        if right_absolute_position.y > left_absolute_position.y:
            rel_angle = -rel_angle

        angle1 = math.acos(l / self.left_radius)
        angle2 = math.acos((dist - l) / self.right_radius)
        self.left_start_angle = rel_angle + angle1
        self.left_stop_angle = rel_angle - angle1
        self.right_start_angle = rel_angle + math.radians(180) + angle2
        self.right_stop_angle = rel_angle + math.radians(180) - angle2

    def draw(self, screen):
        left_absolute_position = self.position + self.left_position
        right_absolute_position = self.position + self.right_position
        left_rect = pygame.Rect(
            left_absolute_position.x - self.left_radius,
            left_absolute_position.y - self.left_radius,
            self.left_radius * 2,
            self.left_radius * 2)
        right_rect = pygame.Rect(
            right_absolute_position.x - self.right_radius,
            right_absolute_position.y - self.right_radius,
            self.right_radius * 2,
            self.right_radius * 2)
        pygame.draw.arc(screen, "white", left_rect, self.left_start_angle, self.left_stop_angle , 2)
        pygame.draw.arc(screen, "white", right_rect, self.right_start_angle, self.right_stop_angle , 2)

    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap()

    def wrap(self):
        margin = 20
        left_absolute_position = self.position + self.left_position
        right_absolute_position = self.position + self.right_position

        if right_absolute_position.x + self.right_radius + margin < 0:
            self.position.x = self.radius + SCREEN_WIDTH + margin
        if left_absolute_position.x - self.left_radius - margin > SCREEN_WIDTH:
            self.position.x = -self.radius - margin
        if max(left_absolute_position.y + self.left_radius, right_absolute_position.y + self.right_radius) + margin < 0:
            self.position.y = self.radius + SCREEN_HEIGHT + margin
        if min(left_absolute_position.y - self.left_radius, right_absolute_position.y - self.right_radius) - margin > SCREEN_HEIGHT:
            self.position.y = -self.radius - margin

    def split(self):
        self.kill()
        score = self.radius * ASTEROID_SCORE_FACTOR
        if self.radius <= ASTEROID_MIN_RADIUS:
            return score

        angle = random.uniform(20, 50)
        vec1 = self.velocity.rotate(angle)
        vec2 = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        ast1 = Asteroid(self.position.x, self.position.y, new_radius)
        ast1.velocity = vec1 * 1.2
        ast2 = Asteroid(self.position.x, self.position.y, new_radius)
        ast2.velocity = vec2 * 1.2
        return score

    def is_point_inside(self, point):
        left_absolute_position = self.position + self.left_position
        left_distance = left_absolute_position.distance_to(point)
        if left_distance <= self.left_radius:
            return True

        right_absolute_position = self.position + self.right_position
        right_distance = right_absolute_position.distance_to(point)
        if right_distance <= self.right_radius:
            return True

        return False
