import pygame
from const import *

class Boss:
    def __init__(self, x, y, speed=10):
        self.spritesheet = pygame.image.load("sprites/boss.png")
        self.frames = []
        for i in range(4):
            frame = self.spritesheet.subsurface((i*32, 0, 32, 32))
            self.frames.append(frame)
            
        self.current_frame = 0
        self.frame_speed = 6
        self.frame_counter = 0

        self.x = x
        self.y = 0 + self.frames[0].get_height()*2
        self.speed = speed
        self.rect = self.frames[0].get_rect()

        self.vida = 400
        self.alive = True


    def update_animation(self):
        self.frame_counter += 0.25
        if self.frame_counter >= self.frame_speed:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)


    def move(self):
        self.x += self.speed

        frame = self.frames[self.current_frame]
        scale_w = int(frame.get_width() * 3.5)

        # se sair completamente da direita, vai para a esquerda
        if self.x - scale_w//2 > wdt:  
            self.speed = -abs(self.speed)  # inverte velocidade

        # se sair completamente da esquerda, vai para a direita
        elif self.x + scale_w//2 < 0:  
            self.speed = abs(self.speed)

        # atualiza o rect centralizado
        scale_h = int(frame.get_height() * 3.5)
        self.rect = frame.get_rect(center=(self.x, self.y))

        # animação
        self.update_animation()


    def draw(self, screen):
         # pega o frame atual
        frame = self.frames[self.current_frame]
        # escala
        scale_w, scale_h = int(frame.get_width() * 3.5), int(frame.get_height() * 3.5)
        frame = pygame.transform.scale(frame, (scale_w, scale_h))
        
        # atualiza o rect centralizado
        self.rect = frame.get_rect(center=(self.x, self.y))
        
        # desenha o sprite
        screen.blit(frame, self.rect.topleft)


    def draw_health_bar(self, screen):
        bar_width = 200
        bar_height = 20
        x = wdt // 2 - bar_width // 2
        y = 0  # topo da tela
        # fundo da barra
        pygame.draw.rect(screen, (80, 80, 80), (x, y, bar_width, bar_height))
        # barra real
        vida_ratio = self.vida / 400  # 400 é vida máxima
        pygame.draw.rect(screen, (200, 0, 0), (x, y, int(bar_width * vida_ratio), bar_height))
        # borda
        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)


