import pygame
from const import verde, vermelho

def draw_hud(screen, player, stage, points_font, stage_font):
    # --- Pontuação e fase ---
    points_render = points_font.render(f"SCORE {player.pontos}", True, (255, 255, 255))
    stage_render = stage_font.render(f"STAGE {stage}", True, (255, 255, 255))

    screen.blit(points_render, (10, 30))
    screen.blit(stage_render, (10, 60))

    # --- Energia ---
    max_height = 100   # altura fixa
    bar_width = 14     # largura fixa
    x = 10             # deixa mais à esquerda
    y = 100            # alinhamento fixo

    # borda da barra
    pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, max_height), 2)

    # calcula energia proporcional
    energia_ratio = max(player.vida, 0) / 100
    energia_height = int(max_height * energia_ratio)
    energia_y = y + (max_height - energia_height)

    # cor dependendo do valor
    color = verde if player.vida >= 50 else vermelho

    # preenchimento da energia
    pygame.draw.rect(screen, color, (x + 2, energia_y, bar_width - 4, energia_height))

    # quadrado amarelo do raio (abaixo da barra)
    pygame.draw.rect(screen, (255, 255, 0), (x, y + max_height + 6, bar_width, bar_width))
