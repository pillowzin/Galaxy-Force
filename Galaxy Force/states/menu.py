import pygame
from const import wdt, hgt
from random import randint

pygame.mixer.init()
pygame.font.init()
volume_bkmusic = 0.1
pygame.mixer.music.load("sounds/background_music.mp3")
pygame.mixer.music.set_volume(volume_bkmusic)

def MENU(screen, player, effects_surface):
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)

    def MainMenu():
        nonlocal effects_surface
        title_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 36)
        subtitle_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 10)
        start_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 10)

        titleA = title_font.render("Galaxy", True, (255, 30, 0))
        titleB = title_font.render("Force", True, (0, 30, 255))
        credit_text = subtitle_font.render("feito por jakezin", True, (255, 255, 255))

        current_time = pygame.time.get_ticks()
        show_start = (current_time // 500) % 2 == 0

        if effects_surface is None:
            effects_surface = pygame.Surface((wdt, hgt))
            effects_surface.fill((0, 0, 0))
            for i in range(200):
                pygame.draw.rect(
                    effects_surface,
                    (randint(0, 255), randint(0, 255), randint(0, 255)),
                    (randint(0, wdt), randint(0, hgt), 2, 2),
                )

        screen.fill((0, 0, 0))
        screen.blit(effects_surface, (0, 0))

        screen.blit(titleA, (wdt // 2 - titleA.get_width() // 2, hgt // 8))
        screen.blit(titleB, (wdt // 2 - titleB.get_width() // 2, hgt // 8 + 40))
        screen.blit(player.img, (wdt//2 - player.img.get_width() - titleA.get_width()//2 + 8, hgt // 4 - player.img.get_height()))
        screen.blit(player.img, (wdt//2 + player.img.get_width() + titleA.get_width()//3, hgt // 4 - player.img.get_height()))

        if show_start:
            start_text = start_font.render(
                "Pressione 'SPACE' para Iniciar", True, (255, 255, 0)
            )
            shadow = start_font.render(
                "Pressione 'SPACE' para Iniciar", True, (0, 0, 0)
            )
            x = wdt // 2 - start_text.get_width() // 2
            y = hgt // 4 + 40
            screen.blit(shadow, (x + 2, y + 2))
            screen.blit(start_text, (x, y))

        screen.blit(credit_text, (wdt // 2 - credit_text.get_width() // 2, titleB.get_height() + credit_text.get_height()))

    MainMenu()
    return effects_surface

