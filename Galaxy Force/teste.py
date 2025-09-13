import pygame
from const import wdt, hgt
from objects.boss import Boss
from objects.player import Player  # só pra sprite
from objects.bullet import Bullet
from objects.enemy_bullet import EnemyBullet
from effects.explosion import Explosion
from effects.damage_text import DamageText

pygame.init()
WINDOW_WIDTH = wdt
WINDOW_HEIGHT = hgt

# --- Janela ---
screen = pygame.display.set_mode((wdt, hgt))
pygame.display.set_caption("Teste Boss")
clock = pygame.time.Clock()

# --- Objetos ---
player = Player('sprites/spaceship.png')
player.rect.centerx = WINDOW_WIDTH // 2
player.rect.bottom = WINDOW_HEIGHT - 50

boss = Boss(WINDOW_WIDTH // 2, 100, speed=2)

bullets = []
enemy_bullets = []
explosions = []
damage_texts = []

bullet_cooldown = 0
explosion_spritesheet = pygame.image.load('sprites/explosion.png').convert_alpha()

# --- Funções ---
def update_bullets(bullets_list, target=None):
    for b in bullets_list[:]:
        if isinstance(b, EnemyBullet):
            b.move(WINDOW_WIDTH, WINDOW_HEIGHT)
        else:
            b.move()
        b.draw(screen)

        if b.off_screen(WINDOW_HEIGHT):
            bullets_list.remove(b)
            continue

        if target and getattr(target, "alive", True) and b.collide(target):
            # chama take_damage se o alvo tiver esse método, senão reduz vida
            if hasattr(target, "take_damage"):
                target.take_damage(10)
            else:
                target.vida -= 10

            # cria o dano visual (flutuante)
            damage_texts.append(DamageText(
                target.rect.centerx,
                target.rect.top,
                "-10",
                color=(255, 0, 0),
                rise_speed=2,
                fade_speed=8,
                target=target
            ))

            bullets_list.remove(b)


def update_explosions(explosions_list):
    for exp in explosions_list[:]:
        exp.update()
        exp.draw(screen)
        if exp.is_finished():
            explosions_list.remove(exp)

# --- Loop principal ---
running = True
while running:
    dt = clock.tick(60)
    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # disparo do player
    if bullet_cooldown == 0 and keys[pygame.K_q]:
        bullets.append(Bullet(player.rect.centerx - 3, player.rect.top))
        bullet_cooldown = 10
    if bullet_cooldown > 0:
        bullet_cooldown -= 1

    # atualiza balas e cria dano
    update_bullets(bullets, boss)
    update_bullets(enemy_bullets)

    # boss
    if boss.alive:
        boss.move(dt)
        boss.try_shoot(enemy_bullets)
        boss.draw(screen)
        boss.draw_health_bar(screen)

        if boss.vida <= 0 and boss.alive:
            boss.alive = False
            if not getattr(boss, "dead", False):
                boss.dead = True
                explosions.append(Explosion(
                    boss.rect.centerx - (Explosion.FRAME_WIDTH * Explosion.SCALE) // 2,
                    boss.rect.centery - (Explosion.FRAME_HEIGHT * Explosion.SCALE) // 2,
                    explosion_spritesheet
                ))

    # player
    player.update()
    player.draw(screen)

    # explosões
    update_explosions(explosions)

    # textos de dano (pisca e sobe)
    for dt_text in damage_texts[:]:
        dt_text.update()
        dt_text.draw(screen)
        if dt_text.is_finished():
            damage_texts.remove(dt_text)

    pygame.display.flip()

pygame.quit()
