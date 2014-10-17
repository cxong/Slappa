import assets
import pygame
from point import *


class Image(object):
    def __init__(self, game, x, y, key, scale=Point(1, 1)):
        self.game = game
        self.__width = 0
        self.__height = 0
        self.__smoothed = True
        if key != '':
            self.__image = assets.images[key]
            self.__width = self.__image.get_width() * scale.x
            self.__height = self.__image.get_height() * scale.y
            self.__set_scale()
        else:
            self.__image = None
            self.image = None
        self.x = x
        self.y = y
        self.anchor = Point(0.5, 0.5)
        self.alpha = 1.0

    def __set_scale(self):
        if self.__image:
            if self.smoothed:
                self.image = pygame.transform.smoothscale(
                    self.__image, (self.__width, self.__height))
            else:
                self.image = pygame.transform.scale(
                    self.__image, (self.__width, self.__height))
    @property
    def width(self):
        return self.__width
    @width.setter
    def width(self, value):
        self.__width = int(value)
        self.__set_scale()
    @property
    def height(self):
        return self.__height
    @height.setter
    def height(self, value):
        self.__height = int(value)
        self.__set_scale()
    @property
    def smoothed(self):
        return self.__smoothed
    @smoothed.setter
    def smoothed(self, value):
        self.__smoothed = value
        self.__set_scale()

    def set_scale(self, scale):
        self.__width = int(self.__width * scale.x)
        self.__height = int(self.__height * scale.y)
        self.__set_scale()


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