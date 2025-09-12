import pygame

class Explosion:
    FRAME_WIDTH = 32
    FRAME_HEIGHT = 32
    SCALE = 2  # você pode mudar pra deixar maior ou menor

    def __init__(self, x, y, sprite_sheet):
        self.x = x
        self.y = y

        self.frames = []
        self.current_frame = 0
        self.frame_speed = 4
        self.frame_counter = 0
        self.finished = False

        # cortar o spritesheet
        for i in range(5):  # 5 frames horizontais
            frame = sprite_sheet.subsurface(
                pygame.Rect(i * self.FRAME_WIDTH, 0, self.FRAME_WIDTH, self.FRAME_HEIGHT)
            )
            frame = pygame.transform.scale(
                frame, (frame.get_width() * self.SCALE, frame.get_height() * self.SCALE)
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
