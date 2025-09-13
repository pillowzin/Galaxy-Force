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
import states.playing as playing

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

# --- Estados ---
game_state = 'menu'
effects_surface = None
bullet_cooldown = 0
game_start_timer = 0  # timer do "Pronto?"

# --- Efeitos ---
explosion_spritesheet = pygame.image.load('sprites/explosion.png').convert_alpha()
explosions = []
stars = [Star() for _ in range(50)]

# --- Fade e música ---
fade_alpha = 255
volume_bkmusic = 0.0
target_volume = 0.1
fade_duration = 5000
pygame.mixer.music.load("sounds/background_music.mp3")
pygame.mixer.music.set_volume(volume_bkmusic)

# --- Loop principal ---
while True:
    player.vida = 1000
    screen.fill((0, 0, 0))
    dt = clock.tick(60)
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
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
        # Fade de volume gradual
        volume_bkmusic = min(volume_bkmusic + (target_volume / fade_duration) * dt, target_volume)
        pygame.mixer.music.set_volume(volume_bkmusic)

        effects_surface = MENU(screen, player, effects_surface, clock, volume_bkmusic)

        if keys[pygame.K_SPACE]:
            playing.player_death = None
            bullets.clear()
            playing.enemy_bullets.clear()
            enemies = get_inimigos_para_fase(1)
            stage = 1
            player.vida = 100
            player.pontos = 0
            game_start_timer = 0
            game_state = 'preparar'

    # --- Preparar / Tela Pronto ---
    elif game_state == 'preparar':
        game_state, stage, bullet_cooldown, game_start_timer = PLAYING(
            screen, player, enemies, bullets, stage, keys,
            bullet_cooldown, explosion_spritesheet, explosions, clock,
            preparing=True, game_start_timer=game_start_timer
        )

    # --- Jogando ---
    elif game_state == 'jogando':
        for star in stars:
            star.move()
            star.draw(screen)

        game_state, stage, bullet_cooldown, game_start_timer = PLAYING(
            screen, player, enemies, bullets, stage, keys,
            bullet_cooldown, explosion_spritesheet, explosions, clock,
            preparing=False, game_start_timer=game_start_timer
        )

    # --- Game Over ---
    elif game_state == 'game_over':
        game_state, player, enemies, bullets, stage = GAMEOVER(
            screen, player, enemies, bullets, stage, keys
        )
        # Reseta balas e timer antes de preparar de novo
        if game_state == 'preparar':
            bullets.clear()
            playing.enemy_bullets.clear()
            game_start_timer = 0

    # --- Game Complete ---
    elif game_state == 'game_complete':
        game_state, player, enemies, bullets, stage = GAME_COMPLETE(
            screen, player, enemies, bullets, stage, keys
        )
        # Reseta balas e timer antes de preparar de novo
        if game_state == 'preparar':
            bullets.clear()
            playing.enemy_bullets.clear()
            game_start_timer = 0

    # --- Fade ---
    if fade_alpha > 0:
        fade_surface = pygame.Surface((wdt, hgt))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))
        fade_alpha -= 5

    pygame.display.flip()
