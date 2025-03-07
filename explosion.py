import pygame
import random
from circleshape import CircleShape

def explode(x, y, size, impact_velocity):
    num_particles = size * random.randrange(1, 10) // 20
    particle_speed = impact_velocity.length_squared() / 3000
    base_velocity = impact_velocity.normalize() * particle_speed
    for i in range(num_particles):
        particle_velocity = base_velocity.rotate(360 / num_particles * i + random.random() * 5) * random.random()
        particle_velocity += impact_velocity * 0.01
        lifetime = particle_velocity.length_squared() / 3000
        ExplosionParticle(x, y, particle_velocity, lifetime)

class ExplosionParticle(CircleShape):
    def __init__(self, x, y, velocity, lifetime):
        super().__init__(x, y, 2)
        self.velocity = velocity
        self.lifetime = lifetime

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius)

    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
        self.position += self.velocity * dt
