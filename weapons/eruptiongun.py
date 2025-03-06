from shot import Shot
from constants import PLAYER_SHOOT_SPEED

class EruptionGun():
    def __init__(self):
        self.shoot_cooldown = 2
        self.name = "Eruption Gun"

    def shoot(self, position, direction):
        num_shots = 20
        angle = 360 / num_shots
        for i in range(num_shots):
            shot = Shot(position.x, position.y)
            shot.velocity = direction.rotate(angle * i) * PLAYER_SHOOT_SPEED
