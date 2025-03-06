import pygame
from sys import exit
from constants import *
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

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidField = AsteroidField()
    score = 0
    score_tick_cooldown = SCORE_TICK_COOLDOWN

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
                print("\nGAME OVER!")
                print(f"You scored {score} points :)")
                exit()
            for shot in shots:
                if asteroid.is_colliding(shot):
                    score += asteroid.split()
                    shot.kill()

        screen.fill("black")
        for drawable in drawables:
            drawable.draw(screen)
        
        screen.blit(font.render(f"Score: {score}", True, "white"), (0,0))

        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()

