import pygame
from config import *
from point import *

"""
Style is a dict with the following attributes:
- font (from loader)
- fill (fill color)
"""


class Text(object):
    def __init__(self, game, x, y, text, style):
        self.game = game
        self.text = text
        self.x = x
        self.y = y
        self.style = style
        self.anchor = Point(0.5, 0.5)

    def exists(self):
        return True

    def update(self, time):
        pass

    def draw(self, surface):
        font = self.style['font']
        size = font.size(self.text)
        point = Point(self.x, self.y)
        point.multiply(self.game.scale.scale)
        point.subtract(Point(size[0] * self.anchor.x,
                             size[1] * self.anchor.y))
        surface.blit(font.render(self.text,
                                 FONT_ANTIALIAS,
                                 self.style['fill']),
                     (int(point.x), int(point.y)))
        if DEBUG_DRAW_SPRITE_ANCHOR:
            point = Point(self.x, self.y)
            point.multiply(self.game.scale.scale)
            pygame.draw.circle(surface,
                               (0, 0, 255),
                               (int(point.x), int(point.y)),
                               3,
                               0)