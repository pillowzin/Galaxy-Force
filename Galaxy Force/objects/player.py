import pygame
from const import *

class Player:
    def __init__(self, img_path):
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(
            self.img,
            (int(self.img.get_width() * 1.8), int(self.img.get_height() * 1.8)),
        )

        self.x, self.y = pygame.mouse.get_pos()
        self.rect = self.img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)
        self.pontos = 0
        self.vida = 100000000000000000
        self.laser_sound = pygame.mixer.Sound("sounds/laser_shoot.mp3")
        self.laser_sound.set_volume(0.2)


    def update(self):
        margem = 10

        self.x, self.y = pygame.mouse.get_pos()
        self.rect.center = (self.x, self.y)
        # Limite pro x
        if self.rect.left < margem:
            self.rect.left = margem
        if self.rect.right > wdt - margem:
            self.rect.right = wdt - margem

        # Limite pro y
        if self.rect.bottom > hgt - margem:
            self.rect.bottom = hgt - margem

        self.x, self.y = self.rect.center


    def draw(self, screen):
        screen.blit(self.img, self.rect.topleft)


    def draw_health_bar(self, screen):
        bar_width = 200
        bar_height = 20
        x = wdt // 2 - bar_width // 2
        y = 20  # topo da tela

        # fundo da barra
        pygame.draw.rect(screen, (80, 80, 80), (x, y, bar_width, bar_height))
        # barra real
        vida_ratio = self.vida / 400  # 400 é vida máxima
        pygame.draw.rect(screen, (200, 0, 0), (x, y, int(bar_width * vida_ratio), bar_height))
        # borda
        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)

