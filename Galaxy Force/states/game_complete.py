import pygame
from const import wdt, hgt

def GAME_COMPLETE(screen, player, enemies, bullets, stage, keys):
    screen.fill((0, 0, 0))
    pygame.mouse.set_visible(True)

    complete_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 20)
    complete_render = complete_font.render("PARABÉNS!", True, (0, 255, 0))

    score_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 16)
    score_render = score_font.render(f"SCORE FINAL: {player.pontos}", True, (255, 255, 255))

    restart_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 12)
    restart_render = restart_font.render("Pressione 'R' para voltar ao menu.", True, (255, 255, 0))

    screen.blit(complete_render, (wdt//2 - complete_render.get_width()//2, hgt//2 - 80))
    screen.blit(score_render, (wdt//2 - score_render.get_width()//2, hgt//2))
    screen.blit(restart_render, (wdt//2 - restart_render.get_width()//2, hgt//2 + 50))

    if keys[pygame.K_r]:
        from mechanics.enemyFactory import get_inimigos_para_fase
        from objects.player import Player
        player = Player("sprites/spaceship.png")
        enemies = get_inimigos_para_fase(1)
        bullets.clear()
        stage = 1
        return "menu", player, enemies, bullets, stage

    return "game_complete", player, enemies, bullets, stage

