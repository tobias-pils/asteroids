from math import radians
import pygame
from constants import BOMB_COOLDOWN

class Ui():
    def __init__(self):
        self.font = pygame.font.Font(None, 25)

    def draw_ui(self, screen, gamestate):
        screen.blit(self.font.render(f"Score: {gamestate.score}", True, "white"), (0, 0))
        screen.blit(self.font.render(f"Lives: {gamestate.player.lives}", True, "white"), (0, 30))

        top = 60
        for i in range(len(gamestate.player.weapons)):
            if i == gamestate.player.selected_weapon:
                self.font.bold = True
            text = f"{i + 1}  {gamestate.player.weapons[i].name}"
            text_rect = screen.blit(self.font.render(text, True, "white"), (0, top))
            if i == gamestate.player.selected_weapon:
                x = text_rect.left + text_rect.width + 4
                y1 = text_rect.top + text_rect.height
                cooldown_ratio = (
                    (gamestate.player.weapons[i].shoot_cooldown - gamestate.player.shoot_cooldown_timer)
                    / gamestate.player.weapons[i].shoot_cooldown
                )
                y2 = y1 - cooldown_ratio * text_rect.height
                pygame.draw.line(screen, "white", (x, y1), (x, y2), 4)
            self.font.bold = False
            top += 20

        if gamestate.player.bomb_cooldown_timer <= 0:
            self.font.bold = True
        text = "E  Bomb"
        text_rect = screen.blit(self.font.render(text, True, "white"), (0, top))
        self.font.bold = False
        x = text_rect.left + text_rect.width + 6
        y1 = text_rect.top + text_rect.height
        cooldown_ratio = (
            (BOMB_COOLDOWN - gamestate.player.bomb_cooldown_timer)
            / BOMB_COOLDOWN
        )
        y2 = y1 - cooldown_ratio * text_rect.height
        pygame.draw.line(screen, "white", (x, y1), (x, y2), 6)
