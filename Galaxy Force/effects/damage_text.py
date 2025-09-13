import pygame

class DamageText:
    def __init__(self, x, y, text, color=(255,0,0), rise_speed=2, fade_speed=3, target=None):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.alpha = 255
        self.rise_speed = rise_speed
        self.fade_speed = fade_speed
        self.font = pygame.font.Font("misc/PressStart2P-Regular.ttf", 14)
        self.target = target

    def update(self):
        if self.target:  # se tiver target, segue ele
            self.x = self.target.rect.centerx
            self.y = self.target.rect.top + self.font.get_height()
        self.y -= self.rise_speed
        self.alpha -= self.fade_speed
        if self.alpha < 0:
            self.alpha = 0

    def draw(self, screen):
        # render principal
        surf = self.font.render(self.text, True, self.color)
        surf.set_alpha(self.alpha)

        # sombra (preta, deslocada 1px)
        shadow = self.font.render(self.text, True, (0, 0, 0))
        shadow.set_alpha(self.alpha)

        screen.blit(shadow, (self.x + 1, self.y + 1))  # sombra primeiro
        screen.blit(surf, (self.x, self.y))            # texto em cima

    def is_finished(self):
        return self.alpha == 0
