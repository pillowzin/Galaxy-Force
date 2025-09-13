# objects/enemy_bullet.py
import pygame

class EnemyBullet:
    def __init__(self, x, y, vx, vy, color=(240,130,48), w=6, h=12, bounces_allowed=6):
        # posição como floats pra física mais suave
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.color = color
        self.width = w
        self.height = h
        self.bounces = 0
        self.max_bounces = bounces_allowed
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def move(self, wdt, hgt):
        # update posição
        self.x += self.vx
        self.y += self.vy

        # ricochete nas laterais (left/right)
        if self.x <= 0:
            self.x = 0
            self.vx = -self.vx
            self.bounces += 1
        elif self.x + self.width >= wdt:
            self.x = wdt - self.width
            self.vx = -self.vx
            self.bounces += 1

        # opcional: ricochete no topo ou só deixar sair por cima/baixo?
        # aqui deixamos passar pelo topo/baixo (player precisa esquivar verticalmente).
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (int(self.x), int(self.y), self.width, self.height))

    def off_screen(self, height):
        # consideramos off-screen quando sair verticalmente (topo ou fundo) ou ultrapassar bounces
        return (self.y < -50 or self.y > height + 50) or (self.bounces > self.max_bounces)

    def collide(self, target):
        # target precisa ter rect (player tem)
        bullet_rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        return bullet_rect.colliderect(target.rect)
