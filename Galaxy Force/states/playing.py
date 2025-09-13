import pygame
from const import wdt, hgt, MAX_STAGE
from mechanics.enemyFactory import get_inimigos_para_fase
from objects.bullet import Bullet
from objects.boss import Boss
from objects.enemy_bullet import EnemyBullet
from effects.explosion import Explosion
from effects.damage_text import DamageText
from effects.player_death import PlayerDeath
from effects.stage_cleared import draw_stage_cleared
from ui.hud import draw_hud

explosion_sound = pygame.mixer.Sound("sounds/explosion.mp3")
explosion_sound.set_volume(0.2)

points_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 12)
stage_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 12)

waiting_next_stage = False
waiting_start_time = 0
enemy_bullets = []

damage_texts = []
player_death = None
player_death_timer = 0
game_start_timer = 0
start_delay = 1000  # espera inicial

def PLAYING(
    screen, player, enemies,
    bullets, stage, keys,
    bullet_cooldown, explosion_spritesheet,
    explosions, clock
):
    global waiting_next_stage, waiting_start_time, enemy_bullets
    global damage_texts, player_death, player_death_timer, game_start_timer

    pygame.mouse.set_visible(False)

    # --- Espera inicial ---
    if game_start_timer < start_delay:
        game_start_timer += clock.get_time()
        ready_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 24)
        ready_text = ready_font.render("Pronto?", True, (255, 255, 0))
        screen.blit(ready_text, (wdt//2 - ready_text.get_width()//2, hgt//2 - 20))
        return "jogando", stage, bullet_cooldown

    # --- Player morreu ---
    if player_death:
        player_death.update()
        player_death.draw(screen)
        player_death_timer += clock.get_time()
        if player_death_timer >= 1000:
            player_death = None
            player_death_timer = 0
            return "game_over", stage, bullet_cooldown
        return "jogando", stage, bullet_cooldown

    # --- Player vivo ---
    player.update()
    player.draw(screen)

    # --- Tiro do Player ---
    if bullet_cooldown == 0 and keys[pygame.K_q]:
        player.laser_sound.play()
        bullets.append(Bullet(player.rect.centerx - 3, player.rect.top))
        bullet_cooldown = 10
    if bullet_cooldown > 0:
        bullet_cooldown -= 1

    # --- Inimigos ---
    for enemy in enemies[:]:
        if isinstance(enemy, Boss):
            if enemy.alive:
                enemy.move(clock.get_time())
                enemy.try_shoot(enemy_bullets)
                enemy.draw(screen)
                enemy.draw_health_bar(screen)
            else:
                if not getattr(enemy, 'dead', False):
                    enemy.dead = True
                    explosions.append(
                        Explosion(
                            enemy.rect.centerx - (Explosion.FRAME_WIDTH*Explosion.SCALE)//2,
                            enemy.rect.centery - (Explosion.FRAME_HEIGHT*Explosion.SCALE)//2,
                            explosion_spritesheet
                        )
                    )
        else:
            if player.rect.colliderect(enemy.rect):
                player.vida -= 10
                enemies.remove(enemy)
                if player.vida <= 0 and player_death is None:
                    player_death = PlayerDeath(player.rect.centerx, player.rect.centery, explosion_spritesheet)
            enemy.move()
            enemy.draw(screen)

    # --- Balas do Player ---
    for bullet in bullets[:]:
        bullet.move()
        bullet.draw(screen)
        if bullet.off_screen(hgt):
            bullets.remove(bullet)
            continue
        for enemy in enemies[:]:
            if bullet.collide(enemy):
                if isinstance(enemy, Boss):
                    enemy.take_damage(10)  # chama piscada e reduz vida
                    damage_texts.append(DamageText(enemy.rect.centerx, enemy.rect.top, "-10", target=enemy))
                    if enemy.vida <= 0:
                        enemies.remove(enemy)
                        return "game_complete", stage, bullet_cooldown  # termina o jogo aqui
                else:
                    enemies.remove(enemy)
                player.pontos += 1
                explosions.append(Explosion(enemy.x, enemy.y, explosion_spritesheet))
                explosion_sound.play()
                if bullet in bullets:
                    bullets.remove(bullet)
                break

    # --- Balas do Boss ---
    for b in enemy_bullets[:]:
        b.move(wdt, hgt)
        b.draw(screen)
        if b.off_screen(hgt):
            enemy_bullets.remove(b)
            continue
        if b.collide(player):
            player.vida -= 10
            damage_texts.append(DamageText(player.rect.centerx, player.rect.top, "-10"))
            enemy_bullets.remove(b)
            if player.vida <= 0 and player_death is None:
                player_death = PlayerDeath(player.rect.centerx, player.rect.centery, explosion_spritesheet)

    # --- Explosões ---
    for explosion in explosions[:]:
        explosion.update()
        explosion.draw(screen)
        if explosion.is_finished():
            explosions.remove(explosion)

    # --- Textos de dano ---
    for dt in damage_texts[:]:
        dt.update()
        dt.draw(screen)
        if dt.is_finished():
            damage_texts.remove(dt)

    # --- HUD ---
    draw_hud(screen, player, stage, points_font, stage_font)
    
    # --- Fases ---
    if len(enemies) == 0 and not waiting_next_stage and len(explosions) == 0:
        waiting_next_stage = True
        waiting_start_time = pygame.time.get_ticks()

    # desenha efeito de next fase sem parar o jogo
    if waiting_next_stage:
        acabou = draw_stage_cleared(screen, waiting_start_time, player.rect.y)
        if acabou:
            waiting_next_stage = False
            stage += 1
            player.vida = min(player.vida + 20, 100)
            enemies.clear()
            enemies.extend(get_inimigos_para_fase(stage))
            for enemy in enemies:
                enemy.speed += 2 * stage // 2
    
    # Limita vida
    if player.vida > 100:
        player.vida = 100

    return "jogando", stage, bullet_cooldown
