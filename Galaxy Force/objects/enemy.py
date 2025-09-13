import pygame
import math
from const import wdt, hgt
from random import randint

class Enemy:
    margem_x = 10

    def __init__(self, sprite_sheet, frame_width, frame_height, x, y, speed):
        self.sprite_sheet = sprite_sheet
        self.frame_width = frame_width
        self.frame_height = frame_height

        self.num_frames = sprite_sheet.get_width() // frame_width
        self.current_frame = 0
        self.frame_speed = 6
        self.frame_counter = 0

        self.x = max(self.margem_x, min(x, wdt - self.margem_x - self.frame_width))
        self.y = y
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, frame_width, frame_height)

        self.wobble_direction = 1
        self.wobble_count = 0
        self.wobble_target_x = self.x

        # tempo até o fim do piscar (timestamp)
        self.hit_until = 0


    def update_animation(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_speed:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % self.num_frames


    def move(self):
        # desce normalmente + oscilação senoidal
        self.y += self.speed + math.sin(pygame.time.get_ticks() * 0.01) * 2  # amplitude 2px, ajuste se quiser mais

        # escolhe novo alvo horizontal a cada 40 ticks
        self.wobble_count += 1
        if self.wobble_count >= 40:
            self.wobble_count = 0
            # alvo aleatório mais distante
            self.wobble_target_x = self.x + randint(-50, 50)
            self.wobble_target_x = max(self.margem_x, min(self.wobble_target_x, wdt - self.margem_x - self.frame_width))

        # aproxima suavemente do alvo
        self.x += (self.wobble_target_x - self.x) * 0.15  # suavidade maior → movimento mais fluido

        # respawn no topo com x aleatório e wobble inicial aleatório
        if self.y >= hgt:
            self.y = -100
            self.x = randint(self.margem_x, wdt - self.margem_x - self.frame_width)
            self.wobble_target_x = self.x

        self.rect.topleft = (self.x, self.y)
        self.update_animation()


    def take_damage(self, dmg=1):
        # seta até quando piscar
        self.hit_until = pygame.time.get_ticks() + 200  # piscar por 200 ms


    def draw(self, screen):
        frame_rect = pygame.Rect(
            self.current_frame * self.frame_width,
            0,
            self.frame_width,
            self.frame_height,
        )

        frame_img = self.sprite_sheet.subsurface(frame_rect)
        frame_img = pygame.transform.rotate(frame_img, 180)

        now = pygame.time.get_ticks()
        if now < self.hit_until:
            if (now // 100) % 2 == 0:
                tmp = frame_img.copy()
                tmp.fill((255, 50, 50), special_flags=pygame.BLEND_RGB_ADD)
                screen.blit(tmp, (self.x, self.y))
                return

        screen.blit(frame_img, (self.x, self.y))
