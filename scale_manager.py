import pygame
from point import *


class ScaleManager(object):
    def __init__(self, game):
        self.game = game
        self.scale = Point(1, 1)
        self.width = game.width
        self.height = game.height

    def setup_scale(self, width, height):
        self.width = width
        self.height = height
        self.scale = Point(float(self.game.width) / width,
                           float(self.game.height) / height)
