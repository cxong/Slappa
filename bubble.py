from sprite import *


class Bubble(Sprite):
    def __init__(self, x, y):
        super(Bubble, self).__init__(x, y, 'explosion')
        self.alpha = 0.7
        self.count = 10

    def update(self, time):
        self.count -= 1
        if self.count <= 0:
            self.health = 0