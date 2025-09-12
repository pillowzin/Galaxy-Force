import pygame
from const import wdt, hgt
from mechanics.enemyFactory import get_inimigos_para_fase
from objects.player import Player

def GAMEOVER(screen, player, enemies, bullets, stage, keys):
    pygame.mixer.music.stop()
    screen.fill((0, 0, 0))
    pygame.mouse.set_visible(True)

    game_over_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 20)
    game_over_render = game_over_font.render("GAME OVER", True, (255, 255, 255))

    try_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 12)
    try_render = try_font.render(
        "Aperte R para tentar novamente.", False, (255, 255, 0)
    )

    screen.blit(game_over_render, (wdt // 2 - 100, hgt // 2 - 180))
    screen.blit(try_render, (wdt // 2 - 180, hgt // 2 - 100))

    if keys[pygame.K_r]:
        pygame.mixer.music.play(-1)
        player = Player("sprites/spaceship.png")
        enemies = get_inimigos_para_fase(1)
        bullets.clear()
        stage = 1
        player.vida = 100
        player.pontos = 0
        return "jogando", player, enemies, bullets, stage

    return "game_over", player, enemies, bullets, stage
