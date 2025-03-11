from weapons.shot import Shot
from constants import PLAYER_SHOOT_SPEED

class ScatterGun():
    def __init__(self):
        self.shoot_cooldown = 0.5
        self.name = "Scatter Gun"

    def shoot(self, position, direction):
        for i in range(-1, 2):
            shot = Shot(position.x, position.y)
            shot.velocity = direction.rotate(30 * i) * PLAYER_SHOOT_SPEED
