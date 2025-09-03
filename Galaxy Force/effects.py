import pygame
from const import *
from random import randint

pygame.mixer.init()


class Explosion:
    def __init__(self, x, y, sprite_sheet):
        self.x = x
        self.y = y

        self.frames = []
        self.current_frame = 0
        self.frame_speed = 4
        self.frame_counter = 0
        self.finished = False

        frame_width = 32
        frame_height = 32

        # cortar o spritesheet
        for i in range(5):
            frame = sprite_sheet.subsurface(
                pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            )
            frame = pygame.transform.scale(
                frame, (frame.get_width() * 2, frame.get_height() * 2)
            )
            self.frames.append(frame)

    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_speed:
            self.frame_counter = 0
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.finished = True

    def draw(self, screen):
        if not self.finished:
            screen.blit(self.frames[self.current_frame], (self.x, self.y))

    def is_finished(self):
        return self.finished


class Star:
    def __init__(self):
        self.x = randint(0, wdt)
        self.y = randint(0, hgt)
        self.speed = randint(1, 3)
        self.size = randint(1, 3)

    def move(self):
        self.y += self.speed
        if self.y > hgt:
            self.y = 0
            self.x = randint(0, wdt)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.size)

