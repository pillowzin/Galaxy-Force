import pygame
from effects.explosion import Explosion

class PlayerDeath:
    def __init__(self, x, y, sprite_sheet):
        self.x = x
        self.y = y
        self.finished = False
        self.explosions = []
        # cria algumas explosões aleatórias ao redor do player
        for i in range(5):
            offset_x = (i-2)*10
            offset_y = (i-2)*10
            self.explosions.append(
                Explosion(self.x + offset_x, self.y + offset_y, sprite_sheet)
            )

    def update(self):
        finished_count = 0
        for exp in self.explosions:
            exp.update()
            if exp.is_finished():
                finished_count += 1
        if finished_count == len(self.explosions):
            self.finished = True

    def draw(self, screen):
        for exp in self.explosions:
            exp.draw(screen)
