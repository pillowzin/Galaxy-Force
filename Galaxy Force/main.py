#IGNORAR O AVISO AVX - não é bug.
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

import pygame
from const import wdt, hgt
from objects.player import Player
from mechanics.enemyFactory import get_inimigos_para_fase
from effects.stars import Star
from states.menu import MENU
from states.playing import PLAYING
from states.game_over import GAMEOVER
from states.game_complete import GAME_COMPLETE

pygame.init()
pygame.mixer.init()

# --- Janela ---
window_icon = pygame.image.load('misc/icon.ico')
pygame.display.set_icon(window_icon)
screen = pygame.display.set_mode((wdt, hgt))
pygame.display.set_caption("Galaxy Forces")
clock = pygame.time.Clock()

# --- Objetos ---
player = Player('sprites/spaceship.png')
stage = 1
enemies = get_inimigos_para_fase(stage)
bullets = []

# --- Estados do jogo ---
game_state = 'menu'
effects_surface = None
bullet_cooldown = 0

# --- Efeitos ---
explosion_spritesheet = pygame.image.load('sprites/explosion.png').convert_alpha()
explosions = []
stars = [Star() for _ in range(50)]

fade_alpha = 255 #fade in ao iniciar
fade_surface = pygame.Surface((wdt, hgt))
fade_surface.fill((0, 0, 0))

# --- Loop principal ---
while True:
    screen.fill((0, 0, 0))
    clock.tick(60)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    # --- Menu ---
    if game_state == 'menu':
        effects_surface = MENU(screen, player, effects_surface, clock)
        if keys[pygame.K_SPACE]:
            game_state = 'jogando'

    # --- Jogando ---
    elif game_state == 'jogando':
        for star in stars:
            star.move()
            star.draw(screen)

        game_state, stage, bullet_cooldown = PLAYING(
            screen, player, enemies, bullets, stage, keys, bullet_cooldown,
            explosion_spritesheet, explosions, clock
        )

    # --- Game Over ---
    elif game_state == 'game_over':
        game_state, player, enemies, bullets, stage = GAMEOVER(
            screen, player, enemies, bullets, stage, keys
        )

    # --- Game Complete ---
    elif game_state == 'game_complete':
        game_state, player, enemies, bullets, stage = GAME_COMPLETE(
            screen, player, enemies, bullets, stage, keys
        )

    if fade_alpha > 0:
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0,0))
        fade_alpha -= 5  # ajusta a velocidade do fade

    pygame.display.flip()
