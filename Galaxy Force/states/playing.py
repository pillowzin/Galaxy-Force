import pygame
from const import wdt, hgt, MAX_STAGE, verde, vermelho
from mechanics.enemyFactory import get_inimigos_para_fase
from objects.bullet import Bullet
from objects.boss import Boss
from effects.explosion import Explosion
from objects.player import Player

explosion_sound = pygame.mixer.Sound("sounds/explosion.mp3")
explosion_sound.set_volume(0.2)

points_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 12)
stage_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 12)

waiting_next_stage = False
waiting_start_time = 0


def PLAYING(
    screen,
    player, enemies,
    bullets, stage, keys,
    bullet_cooldown,
    explosion_spritesheet, explosions,
    clock
):
    global waiting_next_stage, waiting_start_time

    pygame.mouse.set_visible(False)

    stage_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 12)
    points_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 12)
    vidas_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 12)
    damage_texts = []

    # --- HUD ---
    stage_render = stage_font.render(f"STAGE {stage}", True, (255, 255, 255))
    points_render = points_font.render(f"SCORE {player.pontos}", True, (255, 255, 255))
    vidas_render = vidas_font.render(f"ENERGIA {player.vida}", True, (verde))
    if player.vida < 50:
        vidas_render = vidas_font.render(f"ENERGIA {player.vida}", True, (vermelho))
    else:
        vidas_render = vidas_font.render(f"ENERGIA {player.vida}", True, (verde))

    screen.blit(points_render, (10, 30))
    screen.blit(stage_render, (10, 60))
    screen.blit(vidas_render, (wdt - vidas_render.get_width(), 30))


    # --- Player ---
    player.update()
    player.draw(screen)

    # --- Tiro ---
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
                enemy.move()
                enemy.draw(screen)
                enemy.draw_health_bar(screen)
            else:
                # cria explosão uma única vez quando morre
                if not getattr(enemy, 'dead', False):
                    enemy.dead = True
                    exp = Explosion(
                        enemy.rect.centerx - (Explosion.FRAME_WIDTH * Explosion.SCALE) // 2,
                        enemy.rect.centery - (Explosion.FRAME_HEIGHT * Explosion.SCALE) // 2,
                        explosion_spritesheet
                    )
                    explosions.append(exp)
        else:
            # inimigos normais
            if player.rect.colliderect(enemy.rect):
                player.vida -= 10
                enemies.remove(enemy)
                if player.vida <= 0:
                    return "game_over", stage, bullet_cooldown
            enemy.move()
            enemy.draw(screen)

    # --- Balas e colisões ---
    for bullet in bullets[:]:
        bullet.move()
        bullet.draw(screen)
        if bullet.off_screen(hgt):
            bullets.remove(bullet)
            continue
        for enemy in enemies[:]:
            if bullet.collide(enemy):
                if isinstance(enemy, Boss):
                    enemy.vida -= 10  # aplica dano
                    damage_texts.append({
                        'text': "-10",
                        'x': enemy.x + enemy.rect.width // 2,
                        'y': enemy.y,
                        'alpha': 255
                    })
                    if enemy.vida <= 0:
                        enemies.remove(enemy)
                else:
                    enemies.remove(enemy)
                player.pontos += 1
                explosions.append(Explosion(enemy.x, enemy.y, explosion_spritesheet))
                explosion_sound.play()
                if bullet in bullets:
                    bullets.remove(bullet)
                break

    # --- Textos de dano ---
    for dt in damage_texts[:]:
        dmg_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 14)
        dmg_surf = dmg_font.render(dt['text'], True, (255, 255, 0))
        dmg_surf.set_alpha(dt['alpha'])
        screen.blit(dmg_surf, (dt['x'], dt['y']))
        dt['y'] -= 1  # sobe
        dt['alpha'] -= 5  # fade out
        if dt['alpha'] <= 0:
            damage_texts.remove(dt)

    # --- Explosões ---
    for explosion in explosions[:]:
        explosion.update()
        explosion.draw(screen)
        if explosion.is_finished():
            explosions.remove(explosion)

    # --- Verifica se a fase acabou ---
    if len(enemies) == 0 and not waiting_next_stage and len(explosions) == 0:
        waiting_next_stage = True
        waiting_start_time = pygame.time.get_ticks()

    # --- Tela de "PRÓXIMA FASE" ---
    if waiting_next_stage:
        elapsed = pygame.time.get_ticks() - waiting_start_time
        duration = 800
        fade_time = 300

        # alpha para fade in/out
        if elapsed < fade_time:
            alpha = int((elapsed / fade_time) * 255)
        elif elapsed > duration - fade_time:
            alpha = int(((duration - elapsed) / fade_time) * 255)
        else:
            alpha = 255

        msg_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 16)
        msg_surface = msg_font.render("PRÓXIMA FASE!", True, (255, 255, 0))
        msg_surface.set_alpha(alpha)

        # posição centralizado horizontalmente e um pouco acima do player
        x = (wdt - msg_surface.get_width()) // 2
        y = max(player.rect.top - 40, 20)  # 40 pixels acima do player, no mínimo 20 do topo
        screen.blit(msg_surface, (x, y))

        if elapsed >= duration:
            stage += 1
            if stage > MAX_STAGE:
                return 'game_complete', stage, bullet_cooldown
            player.vida += 20
            enemies.clear()
            enemies.extend(get_inimigos_para_fase(stage))
            for enemy in enemies:
                enemy.speed += 2 * stage // 2
            waiting_next_stage = False

    # --- Retorna sempre ---
    return "jogando", stage, bullet_cooldown
