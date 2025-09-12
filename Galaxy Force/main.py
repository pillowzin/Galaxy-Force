import pygame
from const import wdt, hgt
from objects.player import Player
from mechanics.enemyFactory import get_inimigos_para_fase
from effects.stars import Star
from states.menu import MENU
from states.playing import PLAYING
from states.stage_cleared import STAGE_CLEARED
from states.game_over import GAMEOVER
from states.game_complete import GAME_COMPLETE

pygame.init()
pygame.mixer.init()

window_icon = pygame.image.load('misc/icon.ico')
pygame.display.set_icon(window_icon)
screen = pygame.display.set_mode((wdt, hgt))

pygame.display.set_caption("Galaxy Forces")
clock = pygame.time.Clock()
wait_start_time = None
running = True

# objetos
player = Player('sprites/spaceship.png')
stage = 1
enemies = get_inimigos_para_fase(stage)
bullets = []

# estados do jogo
game_state = 'menu'
effects_surface = None
bullet_cooldown = 0

# efeito de explosao
explosion_spritesheet = pygame.image.load('sprites/explosion.png').convert_alpha()
explosions = []

#starsssss
stars = [Star() for _ in range(50)]

# loop do jogo
while running:
    screen.fill((0, 0, 0))
    clock.tick(60)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    if game_state == 'menu':
        effects_surface = MENU(screen, player, effects_surface)
        if keys[pygame.K_SPACE]:
            game_state = 'jogando'

    elif game_state == 'jogando':
        for star in stars:
            star.move()
            star.draw(screen)
        game_state, stage, bullet_cooldown = PLAYING(
            screen, player, enemies, bullets, stage, keys, bullet_cooldown,
            explosion_spritesheet, explosions, clock
        )
        if game_state == 'stage_cleared':
            game_state = 'stage_cleared_state'
            waiting_next_stage = False  # garante que o timer comece do zero

    elif game_state == 'stage_cleared_state':
        acabou = STAGE_CLEARED(screen)
        if acabou:
            stage += 1
            player.vida += 20
            enemies.clear()
            enemies.extend(get_inimigos_para_fase(stage))

            for enemy in enemies:
                enemy.speed += 2 * stage // 2

            game_state = 'jogando'
    elif game_state == 'game_complete':
        game_state, player, enemies, bullets, stage = GAME_COMPLETE(screen, player, enemies, bullets, stage, keys)

    elif game_state == 'game_over':
        game_state, player, enemies, bullets, stage = GAMEOVER(screen, player, enemies, bullets, stage, keys)

    pygame.display.flip()

pygame.quit()