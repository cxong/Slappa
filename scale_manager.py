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
        self.scale = Point(width / float(self.game.width),
                           height / float(self.game.height))
