import random

import pygame

from Entity import Entity


class Ball(Entity):

    def __init__(self, img, speed_start=200, speed_limit=1000):
        super().__init__(img)
        self.dx = speed_start
        self.dy = speed_start
        self.speed_limit = speed_limit

    def move(self, ms_frame):
        pygame.Rect.move_ip(self.rect, self.dx * ms_frame / 1000, self.dy * ms_frame / 1000)
        self.keep_in_border()

    def player_collision(self):
        self.dx = random.uniform(-500, 500) * self.dy / 500
        self.dy = min(max(self.dy * -1.1, -self.speed_limit), self.speed_limit)

    def keep_in_border(self):
        if self.rect.x < self.offset or self.rect.x + self.rect.width > self.screen_x - self.offset:
            self.dx *= -1
        if self.rect.y < self.offset or self.rect.y + self.rect.height > self.screen_y - self.offset:
            self.dy *= -1
