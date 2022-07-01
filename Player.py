from Entity import Entity
from Player_enums import Players


class Player(Entity):
    def __init__(self, img, player: Players, capture):
        super().__init__(img)
        self.player = player
        self.capture = capture

    def move(self, x, y):
        y_offset = 0

        if self.player == Players.PLAYER_1:
            y_offset = self.screen_y / 2

        self.keep_in_border(y_offset + self.offset, y_offset + self.screen_y / 2 - self.offset, self.offset,
                            self.screen_x - self.offset, x, y)

    def keep_in_border(self, min_y, max_y, min_x, max_x, x, y):
        self.rect.x = x - (self.width / 2)
        self.rect.y = y - (self.height / 2)
        if self.rect.x < min_x:
            self.rect.update(min_x, self.rect.y, self.width, self.height)
        if self.rect.x + self.rect.width > max_x:
            self.rect.update(max_x - self.width, self.rect.y, self.width, self.height)
        if self.rect.y < min_y:
            self.rect.update(self.rect.x, min_y, self.width, self.height)
        if self.rect.y + self.rect.height > max_y:
            self.rect.update(self.rect.x, max_y - self.width, self.width, self.height)
