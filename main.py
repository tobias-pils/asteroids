import pygame
from sys import exit
from constants import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SCORE_TICK_AMOUNT,
    SCORE_TICK_COOLDOWN
)
from explosion import ExplosionParticle, explode
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    updatables = pygame.sprite.Group()
    drawables = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatables, drawables)
    Asteroid.containers = (updatables, drawables, asteroids)
    AsteroidField.containers = (updatables)
    Shot.containers = (updatables, drawables, shots)
    ExplosionParticle.containers = (updatables, drawables)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    AsteroidField()

    score = 0
    score_tick_cooldown = SCORE_TICK_COOLDOWN
    lives = 3

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    font = pygame.font.Font(None, 25)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        score_tick_cooldown -= dt
        if score_tick_cooldown < 0:
            score += SCORE_TICK_AMOUNT
            score_tick_cooldown += SCORE_TICK_COOLDOWN

        updatables.update(dt)

        for asteroid in asteroids:
            if player.is_colliding(asteroid):
                if lives == 0:
                    print("\nGAME OVER!")
                    print(f"You scored {score} points :)")
                    exit()
                lives -= 1
                for a in asteroids:
                    a.kill()
                player.respawn()
                break
            for shot in shots:
                if asteroid.is_colliding(shot):
                    asteroid_score = asteroid.split()
                    if asteroid_score > 0:
                        score += asteroid_score
                        explode(
                                asteroid.position.x,
                                asteroid.position.y,
                                asteroid_score,
                                shot.velocity
                                )
                    shot.kill()

        screen.fill("black")
        for drawable in drawables:
            drawable.draw(screen)

        screen.blit(font.render(f"Score: {score}", True, "white"), (0, 0))
        screen.blit(font.render(f"Lives: {lives}", True, "white"), (0, 30))

        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
