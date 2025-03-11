import explosion
from constants import ASTEROID_MIN_RADIUS, ASTEROID_SCORE_FACTOR
from score import score_add

def check_asteroid_collision(gamestate):
    for asteroid in gamestate.groups["asteroids"]:
        is_colliding = None
        for point in gamestate.player.triangle():
            if asteroid.is_overlapping(point):
                is_colliding = asteroid
                break
        if is_colliding != None:
            if gamestate.player.is_shielded:
                gamestate.player.is_shielded = False
                asteroid.kill()
                explosion.explode(
                        asteroid.position.x,
                        asteroid.position.y,
                        ASTEROID_MIN_RADIUS * ASTEROID_SCORE_FACTOR,
                        gamestate.player.velocity * 5
                        )
            else:
                if gamestate.player.lives == 0:
                    print("\nGAME OVER!")
                    print(f"You scored {gamestate.score} points :)")
                    exit()
                gamestate.player.lives -= 1
                for a in gamestate.groups["asteroids"]:
                    a.kill()
                for s in gamestate.groups["shots"]:
                    s.kill()
                for c in gamestate.groups["collectibles"]:
                    c.kill()
                gamestate.player.dead = True
                break
        for shot in gamestate.groups["shots"]:
            if asteroid.is_overlapping(shot.position):
                asteroid_score = asteroid.split()
                if asteroid_score > 0:
                    score_add(asteroid_score, gamestate)
                    explosion.explode(
                            asteroid.position.x,
                            asteroid.position.y,
                            asteroid_score,
                            shot.velocity
                            )
                shot.kill()
        for blast in gamestate.groups["blasts"]:
            if asteroid.is_overlapping(blast.position, blast.radius):
                asteroid_score = asteroid.split()
                if asteroid_score > 0:
                    score_add(asteroid_score, gamestate)
                    explosion.explode(
                            asteroid.position.x,
                            asteroid.position.y,
                            asteroid_score,
                            asteroid.velocity
                            )

def check_collectible_collision(gamestate):
    for collectible in gamestate.groups["collectibles"]:
        is_colliding = False
        for point in gamestate.player.triangle():
            if collectible.is_point_inside(point):
                is_colliding = True
                break
        if not is_colliding:
            for point in collectible.points():
                if gamestate.player.is_point_inside(point):
                    is_colliding = True
                    break
        if is_colliding:
            if collectible.apply_to_player(gamestate.player):
                collectible.kill()
