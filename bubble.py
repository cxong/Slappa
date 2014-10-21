from config import *
from image import *


class Bubble(Image):
    def __init__(self, game, x, y):
        super(Bubble, self).__init__(game, x, y, 'explosion')
        self.alpha = 0.7
        self.count = 10
        self.__exists = True

    def update(self, time):
        self.count -= self.game.config.ANIM_FRAME_RATE / self.game.config.FRAME_RATE
        if self.count <= 0:
            self.__exists = False

    def exists(self):
        return self.__exists