import pygame
from const import wdt, hgt
from objects.player import Player

NEXT_STAGE_DURATION = 1500

def draw_stage_cleared(screen, start_time, y):
    elapsed = pygame.time.get_ticks() - start_time

    # Calcula alpha para fade in/out
    if elapsed < 500:
        alpha = int((elapsed / 500) * 255)  # fade in nos primeiros 0.5s
    elif elapsed > NEXT_STAGE_DURATION - 500:
        alpha = int(((NEXT_STAGE_DURATION - elapsed) / 500) * 255)  # fade out nos últimos 0.5s
    else:
        alpha = 255

    # Renderiza o texto com cor laranja (#EB983F)
    msg_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 18)
    msg_surface = msg_font.render("Próxima Fase!", True, (235, 152, 63))
    msg_surface.set_alpha(alpha)

    # Centraliza o texto na tela
    x = wdt // 2 - msg_surface.get_width() // 2
    y = y - msg_surface.get_height() * 2

    # Desenha apenas o texto com fade
    screen.blit(msg_surface, (x, y))

    return elapsed >= NEXT_STAGE_DURATION
