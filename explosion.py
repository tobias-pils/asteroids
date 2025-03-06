import pygame
import random
from explosionparticle import ExplosionParticle

class Explosion():
    def __init__(self, x, y, size, impact_velocity):
        num_particles = size * random.randrange(1, 5) // 20
        particle_speed = impact_velocity.length_squared() / 3000
        base_velocity = impact_velocity.normalize() * particle_speed
        for i in range(num_particles):
            particle_velocity = base_velocity.rotate(360 / num_particles * i + random.random() * 5) * random.random()
            particle_velocity += impact_velocity * 0.01
            self.spawn_particle(x, y, particle_velocity)

    def spawn_particle(self, x, y, velocity):
        ExplosionParticle(x, y, velocity)

