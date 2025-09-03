import pygame
from random import randint
from objects import *
from const import *
from effects import *
from enemyFactory import get_inimigos_para_fase

pygame.mixer.init()

pygame.mixer.music.load("sounds/background_music.mp3")
pygame.mixer.music.set_volume(0.1)

explosion_sound = pygame.mixer.Sound("sounds/explosion.mp3")
explosion_sound.set_volume(0.2)

points_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 12)
stage_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 12)

waiting_next_stage = False
waiting_start_time = 0
next_stage_duration = 2500


def MENU(screen, player, effects_surface):
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)

    def MainMenu():
        nonlocal effects_surface
        title_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 36)
        subtitle_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 10)
        start_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 10)

        titleA = title_font.render("GALA", True, (255, 30, 0))
        titleB = title_font.render("AGA", True, (0, 30, 255))
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
        screen.blit(player.img, (titleA.get_width() // 2 + 50, hgt // 8 + 35))
        screen.blit(
            player.img,
            (titleA.get_width() // 2 + titleA.get_width() + 80, hgt // 8 + 35),
        )

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

        screen.blit(credit_text, (wdt // 2 - credit_text.get_width() // 2, hgt // 3.8))

    MainMenu()
    return effects_surface


def PLAYING(
    screen,
    player,
    enemies,
    bullets,
    stage,
    keys,
    bullet_cooldown,
    explosion_spritesheet,
    explosions,
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
    vidas_render = vidas_font.render(f"VIDAS {player.vida}", True, (255, 0, 0))

    screen.blit(points_render, (wdt // 2 - 180, 30))
    screen.blit(stage_render, (wdt // 2 - 40, 30))
    screen.blit(vidas_render, (wdt // 2 + 80, 30))



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
            enemy.move()
            enemy.draw(screen)
            enemy.draw_health_bar(screen)
        else:
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
    if len(enemies) == 0 and not waiting_next_stage and len(explosions) == 0 and len(bullets) == 0:
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

def GAME_COMPLETE(screen, player, enemies, bullets, stage, keys):
    screen.fill((0, 0, 0))
    pygame.mouse.set_visible(True)

    complete_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 20)
    complete_render = complete_font.render("PARABÉNS!", True, (0, 255, 0))

    score_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 16)
    score_render = score_font.render(f"SCORE FINAL: {player.pontos}", True, (255, 255, 255))

    restart_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 12)
    restart_render = restart_font.render("Pressione 'R' para jogar de novo.", True, (255, 255, 0))

    screen.blit(complete_render, (wdt//2 - complete_render.get_width()//2, hgt//2 - 80))
    screen.blit(score_render, (wdt//2 - score_render.get_width()//2, hgt//2))
    screen.blit(restart_render, (wdt//2 - restart_render.get_width()//2, hgt//2 + 50))

    if keys[pygame.K_r]:
        from enemyFactory import get_inimigos_para_fase
        from objects import Player
        player = Player("sprites/spaceship.png")
        enemies = get_inimigos_para_fase(1)
        bullets.clear()
        stage = 1
        return "menu", player, enemies, bullets, stage

    return "game_complete", player, enemies, bullets, stage


def GAMEOVER(screen, player, enemies, bullets, stage, keys):
    pygame.mixer.music.stop()
    screen.fill((0, 0, 0))
    pygame.mouse.set_visible(True)

    game_over_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 20)
    game_over_render = game_over_font.render("GAME OVER", True, (255, 255, 255))

    try_font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 12)
    try_render = try_font.render(
        "Aperte R para tentar novamente.", False, (255, 255, 0)
    )

    screen.blit(game_over_render, (wdt // 2 - 100, hgt // 2 - 180))
    screen.blit(try_render, (wdt // 2 - 180, hgt // 2 - 100))

    if keys[pygame.K_r]:
        pygame.mixer.music.play(-1)
        player = Player("sprites/spaceship.png")
        enemies = get_inimigos_para_fase(1)
        bullets.clear()
        stage = 1
        player.vida = 100
        player.pontos = 0
        return "jogando", player, enemies, bullets, stage

    return "game_over", player, enemies, bullets, stage
