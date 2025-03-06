from shot import Shot
from constants import PLAYER_SHOOT_SPEED

class SimpleWeapon():
    def __init__(self):
        self.shoot_cooldown = 0.3
        self.name = "Simple Weapon"

    def shoot(self, position, direction):
        shot = Shot(position.x, position.y)
        shot.velocity = direction * PLAYER_SHOOT_SPEED
