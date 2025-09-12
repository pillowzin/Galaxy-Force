import pygame
from const import wdt, hgt
next_stage_duration = 2500

def STAGE_CLEARED(screen):
    global waiting_next_stage, waiting_start_time

    elapsed = pygame.time.get_ticks() - waiting_start_time

    screen.fill((0, 0, 0))

    if elapsed < 1000:
        alpha = int((elapsed / 1000) * 255)
    elif elapsed > next_stage_duration - 1000:
        alpha = int(((next_stage_duration - elapsed) / 1000) * 255)
    else:
        alpha = 255

    msg_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 18)
    msg_surface = msg_font.render("Próxima Fase!", True, (255, 255, 255))
    msg_surface.set_alpha(alpha)
    x = wdt // 2
    y = hgt // 2

    overlay = pygame.Surface((wdt, hgt))
    overlay.set_alpha(100)
    overlay.fill((0, 0, 0))

    screen.blit(overlay, (0, 0))
    screen.blit(msg_surface, (x, y))

    if elapsed >= next_stage_duration:
        waiting_next_stage = False
        return True  # indica que a transição acabou

    return False

