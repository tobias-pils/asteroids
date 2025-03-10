import pygame
from player import Player
from asteroidfield import AsteroidField
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLAYER_START_LIVES,
    SCORE_TICK_COOLDOWN
)
from asteroid import Asteroid
from shot import Shot
from explosion import ExplosionParticle
from collectibles.shield import Shield
from collectibles.speed import Speed

class GameState():
    def __init__(self):
        self.groups = self.assign_groups()
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_START_LIVES)
        self.asteroidfield = AsteroidField()
        self.score = 0
        self.score_tick_cooldown = SCORE_TICK_COOLDOWN

    def assign_groups(self):
        updatables = pygame.sprite.Group()
        drawables = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        shots = pygame.sprite.Group()
        effects = pygame.sprite.Group()
        collectibles = pygame.sprite.Group()

        Player.containers = (updatables, drawables)
        Asteroid.containers = (updatables, drawables, asteroids)
        AsteroidField.containers = (updatables)
        Shot.containers = (updatables, drawables, shots)
        ExplosionParticle.containers = (updatables, drawables, effects)
        Shield.containers = (updatables, drawables, collectibles)
        Speed.containers = (updatables, drawables, collectibles)

        return {
            "updatables": updatables,
            "drawables":drawables,
            "asteroids": asteroids,
            "shots": shots,
            "effects": effects,
            "collectibles": collectibles
        }
