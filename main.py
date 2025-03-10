from typing import Self
import pygame
from sys import exit
from constants import (
    ASTEROID_MIN_RADIUS,
    ASTEROID_SCORE_FACTOR,
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
from collectibles.shield import Shield

def main():
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
    background_image = pygame.image.load("./assets/space.jpg")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.blit(background_image, (0, 0))

        if player.dead:
            if len(effects) > 0:
                effects.update(dt)
            else:
                player.respawn()
        else:
            score_tick_cooldown -= dt
            if score_tick_cooldown < 0:
                score += SCORE_TICK_AMOUNT
                score_tick_cooldown += SCORE_TICK_COOLDOWN

            updatables.update(dt)

            for asteroid in asteroids:
                is_colliding = None
                for point in player.triangle():
                    if asteroid.is_point_inside(point):
                        is_colliding = asteroid
                        break
                if is_colliding != None:
                    if player.is_shielded:
                        player.is_shielded = False
                        asteroid.kill()
                        explode(
                                asteroid.position.x,
                                asteroid.position.y,
                                ASTEROID_MIN_RADIUS * ASTEROID_SCORE_FACTOR,
                                player.velocity * 5
                                )
                    else:
                        if lives == 0:
                            print("\nGAME OVER!")
                            print(f"You scored {score} points :)")
                            exit()
                        lives -= 1
                        for a in asteroids:
                            a.kill()
                        for s in shots:
                            s.kill()
                        player.dead = True
                        break
                for shot in shots:
                    if asteroid.is_point_inside(shot.position):
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
            for collectible in collectibles:
                is_colliding = False
                for point in player.triangle():
                    if collectible.is_point_inside(point):
                        is_colliding = True
                        break
                if is_colliding:
                    if collectible.apply_to_player(player):
                        collectible.kill()

        for drawable in drawables:
            drawable.draw(screen)

        screen.blit(font.render(f"Score: {score}", True, "white"), (0, 0))
        screen.blit(font.render(f"Lives: {lives}", True, "white"), (0, 30))

        top = 60
        for i in range(len(player.weapons)):
            if i == player.selected_weapon:
                font.bold = True
            text = f"{i + 1}  {player.weapons[i].name}"
            text_rect = screen.blit(font.render(text, True, "white"), (0, top))
            if i == player.selected_weapon:
                x = text_rect.left + text_rect.width + 4
                y1 = text_rect.top + text_rect.height
                cooldown_ratio = (player.weapons[i].shoot_cooldown - player.cooldown_timer) / player.weapons[i].shoot_cooldown
                y2 = y1 - cooldown_ratio * text_rect.height
                pygame.draw.line(screen, "white", (x, y1), (x, y2), 4)
            font.bold = False
            top += 20

        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
