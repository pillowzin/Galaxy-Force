import pygame
from const import verde, vermelho

def draw_hud(screen, player, stage, points_font, stage_font):
    # Pontuação e fase
    points_render = points_font.render(f"SCORE {player.pontos}", True, (255, 255, 255))
    stage_render = stage_font.render(f"STAGE {stage}", True, (255, 255, 255))
    screen.blit(points_render, (10, 30))
    screen.blit(stage_render, (10, 60))

    # Barra de energia
    max_height = 100
    bar_width = 14
    x = 10
    y = 100
    pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, max_height), 2)
    energia_ratio = max(player.vida, 0) / 100
    energia_height = int(max_height * energia_ratio)
    energia_y = y + (max_height - energia_height)
    color = verde if player.vida >= 50 else vermelho
    pygame.draw.rect(screen, color, (x + 2, energia_y, bar_width - 4, energia_height))

    # Ícone de raio
    lightning_img = pygame.image.load("misc/lightning.png").convert_alpha()
    lightning_scale = 28  # aumenta para visualização
    lightning_img = pygame.transform.scale(lightning_img, (lightning_scale, lightning_scale))
    screen.blit(lightning_img, (x - 6, y + max_height + 6))
