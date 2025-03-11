import pygame
from collision import check_asteroid_collision, check_collectible_collision
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from score import score_tick
from ui import Ui
from gamestate import GameState

def main():
    pygame.init()
    gamestate = GameState()
    ui = Ui()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    background_image = pygame.image.load("./assets/space.jpg")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.blit(background_image, (0, 0))

        if gamestate.player.dead:
            if len(gamestate.groups["effects"]) > 0:
                gamestate.groups["effects"].update(dt)
            else:
                gamestate.player.respawn()
        else:
            score_tick(dt, gamestate)

            gamestate.groups["updatables"].update(dt)

            check_asteroid_collision(gamestate)
            check_collectible_collision(gamestate)

        for drawable in gamestate.groups["drawables"]:
            drawable.draw(screen)

        ui.draw_ui(screen, gamestate)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
