import pygame
from circleshape import CircleShape
from constants import BOMB_BLAST_RADIUS, BOMB_DELAY
from weapons.blast import Blast

class Bomb(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, 10)
        self.delay = BOMB_DELAY
        self.__hand_angle = 0

    def update(self, dt):
        self.delay -= dt
        if self.delay < 0:
            self.detonate()
        self.__hand_angle += dt * 360

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)
        hand_vector = pygame.Vector2(0, 1).rotate(self.__hand_angle)
        hand_vector.scale_to_length(self.radius)
        pygame.draw.line(screen, "white", self.position, self.position + hand_vector)

    def detonate(self):
        Blast(self.position.x, self.position.y, BOMB_BLAST_RADIUS)
        self.kill()
