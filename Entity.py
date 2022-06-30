import pygame


class Entity:
    def __init__(self, img, x=100, y=100, width=100, height=100, screen_x=640, screen_y=960, offset=20):
        self.width = width
        self.height = height
        self.img = pygame.transform.scale(img, (width, height))
        self.rect = pygame.Rect(x, y, width, height)
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.offset = offset

    def draw(self, screen):
        screen.blit(self.img, (self.rect.x, self.rect.y))
