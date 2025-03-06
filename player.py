from circleshape import CircleShape
from shot import Shot
from constants import (
    PLAYER_ACCELERATION,
    PLAYER_SHOOT_COOLDOWN,
    PLAYER_SHOOT_SPEED,
    PLAYER_RADIUS,
    PLAYER_MAX_SPEED,
    PLAYER_TURN_SPEED
)
import pygame

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown_timer = 0
        self.init_x = x
        self.init_y = y

    def get_forward(self):
        return pygame.Vector2(0, 1).rotate(self.rotation)

    def respawn(self):
        self.velocity = pygame.Vector2(0, 0)
        self.position.x = self.init_x
        self.position.y = self.init_y
        self.rotation = 0

    def triangle(self):
        forward = self.get_forward()
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def accelerate_move(self, dt):
        self.velocity += self.get_forward() * dt * PLAYER_ACCELERATION
        self.velocity.clamp_magnitude_ip(PLAYER_MAX_SPEED)

    def move(self, dt):
        self.position += self.velocity * dt

    def update(self, dt):
        if self.cooldown_timer < dt:
            self.cooldown_timer = 0
        elif self.cooldown_timer > 0:
            self.cooldown_timer -= dt

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.accelerate_move(dt)
        if keys[pygame.K_s]:
            self.accelerate_move(-dt)
        self.move(dt)

        if keys[pygame.K_SPACE] and self.cooldown_timer == 0:
            self.cooldown_timer = PLAYER_SHOOT_COOLDOWN
            self.shoot()

    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = forward * PLAYER_SHOOT_SPEED
