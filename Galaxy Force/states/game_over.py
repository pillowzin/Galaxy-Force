import pygame
from const import wdt, hgt
from mechanics.enemyFactory import get_inimigos_para_fase
from objects.player import Player
import states.playing as playing  # para resetar player_death

def GAMEOVER(screen, player, enemies, bullets, stage, keys):
    screen.fill((0, 0, 0))
    pygame.mouse.set_visible(True)

    game_over_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 24)
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (wdt//2 - game_over_text.get_width()//2, hgt//2 - 60))

    try_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 14)
    try_text = try_font.render("Aperte R para voltar ao menu.", True, (255, 255, 0))
    screen.blit(try_text, (wdt//2 - try_text.get_width()//2, hgt//2 + 20))

    if keys[pygame.K_r]:
        playing.player_death = None  # reseta animação
        player = Player("sprites/spaceship.png")
        enemies = get_inimigos_para_fase(1)
        bullets.clear()
        stage = 1
        player.vida = 100
        player.pontos = 0
        return "menu", player, enemies, bullets, stage

    return "game_over", player, enemies, bullets, stage
