import pygame
from const import *
from random import randint

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

