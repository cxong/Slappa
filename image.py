import assets
import pygame
from point import *


class Image(object):
    def __init__(self, x, y, key, scale=Point(1, 1)):
        if key != '':
            self.image = pygame.transform.scale(
                assets.images[key],
                (
                    assets.images[key].get_width() * scale.x,
                    assets.images[key].get_height() * scale.y))
        else:
            self.image = None
        self.x = x
        self.y = y
        self.anchor = Point(0.5, 0.5)
        self.alpha = 1.0

    def update(self, time):
        pass

    def draw(self, surface):
        if self.image is not None:
            self.image.set_alpha(int(self.alpha * 255))
            surface.blit(self.image,
                         (self.x - self.image.get_width() * self.anchor.x,
                          self.y - self.image.get_height() * self.anchor.y))

    def exists(self):
        return True