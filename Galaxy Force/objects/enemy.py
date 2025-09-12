import pygame
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


    def update_animation(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_speed:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % self.num_frames


    def move(self):
        self.y += self.speed

        self.wobble_count += 1
        if self.wobble_count >= 40:
            self.wobble_direction *= -1
            self.wobble_count = 0

        self.x += self.wobble_direction * 2
        self.x = max(self.margem_x, min(self.x, wdt - self.margem_x - self.frame_width))

        if self.y >= hgt:
            self.y = -100

        self.rect.topleft = (self.x, self.y)
        self.update_animation()


    def draw(self, screen):
        frame_rect = pygame.Rect(
            self.current_frame * self.frame_width,
            0,
            self.frame_width,
            self.frame_height,
        )

        frame_img = self.sprite_sheet.subsurface(frame_rect)
        frame_img = pygame.transform.rotate(frame_img, 180)
        screen.blit(frame_img, (self.x, self.y))

