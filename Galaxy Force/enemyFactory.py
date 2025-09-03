from objects import *
from random import randint


def CriarInimigosNormais(n):
    from objects import CriarInimigos

    return CriarInimigos(n)


def CriarInimigosColoridos(n):
    inimigos = []
    for _ in range(n):
        enemy = Enemy(
            enemy2_spritesheet,
            frame_width,
            frame_height,
            randint(0, wdt - frame_width),
            randint(-100, 0),
            randint(3, 5),
        )

        inimigos.append(enemy)
    return inimigos


def CriarMiniBoss(n=1):
    inimigos = []
    for _ in range(n):
        miniboss = Enemy(
            enemy_spritesheet,
            frame_width,
            frame_height,
            wdt // 2 - frame_width // 2,
            randint(-100, 0),
            randint(4, 6),
        )
        inimigos.append(miniboss)
    return inimigos


def CriarBossFinal(n=1):
    from objects import Boss
    return [Boss(wdt // 2 - 65 // 2, 50)]  # 65 é o tamanho do frame do boss


def get_inimigos_para_fase(stage):
    if 1 <= stage <= 3:
        # Só inimigos normais
        return CriarInimigosNormais(8 + stage)  

    elif 4 <= stage <= 5:
        # Metade normais, metade coloridos
        return CriarInimigosNormais(4 + stage) + CriarInimigosColoridos(4 + stage)

    elif 6 <= stage <= 7:
        # Mistura com mais coloridos e miniboss
        return CriarInimigosColoridos(5 + stage) + CriarMiniBoss(1)

    elif stage == 8:
        # Só miniboss
        return CriarMiniBoss(2)

    elif stage == 9:
        # Muitos normais e coloridos
        return CriarInimigosNormais(6) + CriarInimigosColoridos(6)

    elif stage == 10:
        # Boss final
        return CriarBossFinal(1)

    else:
        # Caso padrão (se stage > 10)
        return CriarInimigosNormais(10)