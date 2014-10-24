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
        self.x = x
        self.y = y
        self.anchor = Point(0.5, 0.5)
        font = style['font']
        self.image = font.render(text,
                                 self.game.config.FONT_ANTIALIAS,
                                 style['fill'])
        self.size = font.size(text)
        self.visible = True

    def exists(self):
        return True

    def update(self, time):
        pass

    def draw(self, surface):
        if not self.visible:
            return
        if self.game.config.DEBUG_NO_FONTS:
            return
        point = Point(self.x, self.y)
        point.multiply(self.game.scale.scale)
        point.subtract(Point(self.size[0] * self.anchor.x,
                             self.size[1] * self.anchor.y))
        surface.blit(self.image, (int(point.x), int(point.y)))
        if self.game.config.DEBUG_DRAW_SPRITE_ANCHOR:
            point = Point(self.x, self.y)
            point.multiply(self.game.scale.scale)
            pygame.draw.circle(surface,
                               (0, 0, 255),
                               (int(point.x), int(point.y)),
                               3,
                               0)