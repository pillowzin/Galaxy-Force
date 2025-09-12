import pygame
from const import *
from random import randint
from objects.enemy import Enemy
from objects.boss import Boss

# Carregamento de sprites
def LoadAndResizeSheet(path, frame_width_orig, frame_height_orig, num_frames, scale_factor):
    sprite_sheet = pygame.image.load(path)
    sprite_width_scaled = int(frame_width_orig * num_frames * scale_factor)
    sprite_height_scaled = int(frame_height_orig * scale_factor)
    sprite_sheet = pygame.transform.scale(sprite_sheet, (sprite_width_scaled, sprite_height_scaled))
    frame_width_scaled = int(frame_width_orig * scale_factor)
    frame_height_scaled = int(frame_height_orig * scale_factor)
    return sprite_sheet, frame_width_scaled, frame_height_scaled

enemy_spritesheet, frame_width, frame_height = LoadAndResizeSheet("sprites/enemy.png", 16, 16, 2, 2.5)
enemy2_spritesheet, frame_width2, frame_height2 = LoadAndResizeSheet("sprites/enemy2.png", 16, 16, 2, 2.5)

# Funções de criação de inimigos
def CriarInimigosNormais(n, wdt):
    return [
        Enemy(enemy_spritesheet, frame_width, frame_height, randint(0, wdt - frame_width), randint(-100, 0), randint(2, 4) + randint(0, 3)/2)
        for _ in range(n)
    ]

def CriarInimigosColoridos(n, wdt):
    return [
        Enemy(enemy2_spritesheet, frame_width2, frame_height2, randint(0, wdt - frame_width2), randint(-100, 0), randint(2, 4) + randint(0, 3)/2)
        for _ in range(n)
    ]

def CriarMiniBoss(n=1):
    inimigos = []
    for _ in range(n):
        miniboss = Enemy(enemy_spritesheet, frame_width, frame_height, wdt//2 - frame_width//2, randint(-100,0), randint(4,6))
        inimigos.append(miniboss)
    return inimigos

def CriarBossFinal(n=1):
    return [Boss(wdt//2 - 65//2, 50)]

def get_inimigos_para_fase(stage):
    if 1 <= stage <= 3:
        return CriarInimigosNormais(8 + stage, wdt)
    elif 4 <= stage <= 5:
        return CriarInimigosNormais(4 + stage, wdt) + CriarInimigosColoridos(4 + stage, wdt)
    elif 6 <= stage <= 7:
        return CriarInimigosColoridos(5 + stage, wdt) + CriarMiniBoss(1)
    elif stage == 8:
        return CriarMiniBoss(2)
    elif stage == 9:
        return CriarInimigosNormais(6, wdt) + CriarInimigosColoridos(6, wdt)
    elif stage == 10:
        return CriarBossFinal(1)
    else:
        return CriarInimigosNormais(10, wdt)

