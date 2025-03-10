from constants import SCORE_TICK_AMOUNT, SCORE_TICK_COOLDOWN
from collectibles.shield import Shield

def score_tick(dt, gamestate):
    gamestate.score_tick_cooldown -= dt
    if gamestate.score_tick_cooldown < 0:
        score_add(SCORE_TICK_AMOUNT, gamestate)
        gamestate.score_tick_cooldown += SCORE_TICK_COOLDOWN

def score_add(amount, gamestate):
    old_score = gamestate.score
    gamestate.score += amount
    if gamestate.score // 1000 > old_score // 1000:
        Shield()
