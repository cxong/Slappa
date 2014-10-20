from group import *
from image import *
from sound import *
from sprite import *


class GameObjectFactory(object):
    def __init__(self, game):
        self.game = game

    def audio(self, key):
        return Sound(self.game, key)

    def group(self):
        return self.game.world.add(Group())

    def image(self, x, y, key, scale=Point(1, 1)):
        return self.game.world.add(Image(self.game, x, y, key, scale))

    def sprite(self, x, y, key, scale=Point(1, 1)):
        return self.game.world.add(Sprite(self.game, x, y, key, scale))