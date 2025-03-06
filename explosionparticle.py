import pygame
from circleshape import CircleShape

class ExplosionParticle(CircleShape):
    def __init__(self, x, y, velocity):
        super().__init__(x, y, 2)
        self.velocity = velocity
        self.lifetime = velocity.length_squared() / 2000

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius)

    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
        self.position += self.velocity * dt
    
