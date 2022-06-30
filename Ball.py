import pygame
import random
from Entity import Entity


class Ball(Entity):

    def __init__(self, img):
        super().__init__(img)
        self.dx = 1
        self.dy = 1

    def move(self, screenX, screenY):
        pygame.Rect.move_ip(self.rect, self.dx, self.dy)
        self.keep_in_border(screenX, screenY)

    def player_collision(self):
        self.dx = random.uniform(-5, 5)
        self.dy = (self.dy + 2) * -1

    def keep_in_border(self, screenX, screenY):
        if self.rect.x < 0 or self.rect.x + self.rect.width > screenX:
            self.dx *= -1
        if self.rect.y < 0 or self.rect.y + self.rect.height > screenY:
            self.dy *= -1
