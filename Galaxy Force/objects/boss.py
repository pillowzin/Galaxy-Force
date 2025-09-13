# objects/boss.py
import pygame
import math
import random
from const import *
from objects.enemy_bullet import EnemyBullet

class Boss:
    def __init__(self, x, y, speed=2):  # velocidade menor: 2
        self.spritesheet = pygame.image.load("sprites/boss.png").convert_alpha()
        self.frames = []
        for i in range(4):
            frame = self.spritesheet.subsurface((i*32, 0, 32, 32))
            self.frames.append(frame)
            
        self.current_frame = 0
        self.frame_speed = 6
        self.frame_counter = 0

        self.x = x
        # base y pra onda; o y passado será a base vertical
        self.base_y = y if y is not None else 80
        self.y = self.base_y
        self.speed = speed
        self.rect = self.frames[0].get_rect()

        self.vida = 400
        self.alive = True

        # timer de piscar (timestamp em ms)
        self.hit_until = 0

        # ataque
        self._last_shot = pygame.time.get_ticks()
        self._shot_cd = 900  # ms entre disparos (ajusta aqui)
        self._wave_phase = random.random() * 10  # fase aleatória pra variar onda
        self._time = 0

    def update_animation(self):
        self.frame_counter += 0.25
        if self.frame_counter >= self.frame_speed:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def move(self, dt_ms):
        """Chamado todo frame. dt_ms = tempo desde último frame (clock.tick)."""
        # movimento horizontal contínuo (mais lento)
        self.x += self.speed * (dt_ms / 16.67)  # normaliza por ~60FPS (opcional)
        # rebote simples nas bordas invertendo direção
        frame = self.frames[self.current_frame]
        scale_w = int(frame.get_width() * 3.5)
        if self.x - scale_w//2 > wdt:
            self.speed = -abs(self.speed)
        elif self.x + scale_w//2 < 0:
            self.speed = abs(self.speed)

        # movimento em onda vertical perpétuo
        # usa tempo pra calcular seno (mais orgânico)
        self._time += dt_ms
        amplitude = 40  # altura da onda (ajusta)
        frequency = 0.0015  # velocidade da oscilação (ajusta)
        self.y = self.base_y + math.sin(self._time * frequency + self._wave_phase) * amplitude

        # atualiza rect centralizado
        self.rect = frame.get_rect(center=(int(self.x), int(self.y)))

        # animação
        self.update_animation()


    def draw_health_bar(self, screen):
        bar_width = 200
        bar_height = 20
        x = wdt // 2 - bar_width // 2
        y = 0
        pygame.draw.rect(screen, (80, 80, 80), (x, y, bar_width, bar_height))
        vida_ratio = max(self.vida, 0) / 400
        pygame.draw.rect(screen, (200, 0, 0), (x, y, int(bar_width * vida_ratio), bar_height))
        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)

    # ---------- Ataque simples: ricochete ----------
    def try_shoot(self, bullets_list):
        now = pygame.time.get_ticks()
        if now - self._last_shot < self._shot_cd:
            return
        self._last_shot = now

        # cria 1-3 balas com velocidades iniciais variadas
        n = random.choice((2,3))
        for i in range(n):
            angle = random.uniform(-0.6, 0.6)  # ângulo horizontal inicial em radianos (lateral)
            speed = random.uniform(3.0, 5.5)
            # decide direção lateral aleatória
            dir_x = math.cos(angle)
            dir_y = math.sin(angle) + 0.6  # garante movimento para baixo em geral (player precisa esquivar)
            vx = dir_x * speed
            vy = dir_y * speed
            # cria a bala centrada no boss
            bx = self.x
            by = self.y + 20  # pequeno offset para sair abaixo do boss
            bullets_list.append(EnemyBullet(bx, by, vx, vy))

    # se quiser que o boss acelere quando dano, pode chamar isto quando vida cair
    def set_aggressive(self):
        self._shot_cd = max(300, self._shot_cd - 150)
        self.speed *= 1.15

    # piscar quando toma dano
    def take_damage(self, dmg):
        self.vida -= dmg
        # seta até quando vai piscar (timestamp)
        self.hit_until = pygame.time.get_ticks() + 300  # piscar por 300 ms
        if self.vida <= 0:
            self.alive = False

    def draw(self, screen):
        frame = self.frames[self.current_frame]
        scale_w, scale_h = int(frame.get_width() * 3.5), int(frame.get_height() * 3.5)
        frame = pygame.transform.scale(frame, (scale_w, scale_h))
        self.rect = frame.get_rect(center=(int(self.x), int(self.y)))

        # piscada: se agora < hit_until, alterna cor a cada 100ms
        now = pygame.time.get_ticks()
        if now < self.hit_until:
            if (now // 100) % 2 == 0:
                tmp = frame.copy()
                tmp.fill((255, 50, 50), special_flags=pygame.BLEND_RGB_ADD)
                screen.blit(tmp, self.rect.topleft)
                return

        screen.blit(frame, self.rect.topleft)
