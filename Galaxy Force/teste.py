import pygame
from const import wdt, hgt
from objects.boss import Boss
from objects.player import Player
from objects.bullet import Bullet
from effects.explosion import Explosion

pygame.init()

# janela
screen = pygame.display.set_mode((wdt, hgt))
pygame.display.set_caption("Galaxy Forces")
clock = pygame.time.Clock()

# objetos
player = Player('sprites/spaceship.png')
boss = Boss(wdt // 2, hgt // 2)

bullets = []
bullet_cooldown = 0

explosion_spritesheet = pygame.image.load('sprites/explosion.png')

explosions = []  # lista de explosões

running = True
while running:
    screen.fill((0, 0, 0))
    clock.tick(60)
    keys = pygame.key.get_pressed()

    # eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # disparo
    if bullet_cooldown == 0 and keys[pygame.K_q]:
        player.laser_sound.play()
        bullets.append(Bullet(player.rect.centerx - 3, player.rect.top))
        bullet_cooldown = 10
    if bullet_cooldown > 0:
        bullet_cooldown -= 1

    # balas
    for bullet in bullets[:]:
        bullet.move()
        bullet.draw(screen)

        if bullet.off_screen(hgt):
            bullets.remove(bullet)
            continue

        # colisão com o boss
        if bullet.collide(boss):
            boss.vida -= 10
            print(f"Boss tomou dano! Vida: {boss.vida}")
            bullets.remove(bullet)

    # boss
    if boss.alive:
        boss.move()
        boss.draw_health_bar(screen)
        boss.draw(screen)

    # player
    player.update()
    player.draw(screen)

    # criar explosão apenas uma vez quando o boss morrer
    if boss.vida <= 0 and boss.alive:
        boss.alive = False  # boss desaparece da tela
        if not getattr(boss, "dead", False):  # cria a explosão só uma vez
            boss.dead = True
            boss_center_x = boss.rect.centerx
            boss_center_y = boss.rect.centery

            exp = Explosion(
                boss_center_x - (Explosion.FRAME_WIDTH * Explosion.SCALE) // 2,
                boss_center_y - (Explosion.FRAME_HEIGHT * Explosion.SCALE) // 2,
                explosion_spritesheet
            )
            explosions.append(exp)

    # atualizar e desenhar explosões
    for exp in explosions[:]:
        exp.update()
        exp.draw(screen)
        if exp.is_finished():
            explosions.remove(exp)

    pygame.display.flip()

pygame.quit()
