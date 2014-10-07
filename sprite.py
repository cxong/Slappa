import pygame
from point import *


class Sprite(object):
    def __init__(self,
                 image,
                 scale=Point(1, 1),
                 crop=pygame.Rect(0, 0, 0, 0)):
        self.image = image.convert_alpha()

        self.crop = crop
        self.crop.width *= scale.x
        self.crop.height *= scale.y
        if crop.width == 0 or crop.height == 0:
            self.crop = pygame.Rect(0, 0,
                                    image.get_width() * scale.x,
                                    image.get_height() * scale.y)
        self.width = self.crop.width
        self.height = self.crop.height
        self.image = pygame.transform.scale(
            self.image,
            (image.get_width() * scale.x, image.get_height() * scale.y)).convert_alpha()

        self.dx = 0
        self.dy = 0
        self.x = 0
        self.y = 0

        self.flip_x = False
        self.flip_y = False

        self.health = 0

        self.anchor = Point(0.5, 0.5)

    def update(self, time):
        self.x += self.dx * time
        self.y += self.dy * time

    def draw(self, surface):
        cropped = pygame.Surface(self.crop.size)
        cropped.blit(self.image, (0, 0), self.crop)
        cropped = pygame.transform.flip(cropped, self.flip_x, self.flip_y)
        surface.blit(cropped,
                     (self.x - self.width * self.anchor.x,
                     self.y - self.height * self.anchor.y))