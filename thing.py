import random
from sprite import *


class Thing(Sprite):
    SPEED = 0.3

    def __init__(self, x, y, key, target):
        super(Thing, self).__init__(x, y, key)

        self.allow_rotations = True
        self.rotation = random.randint(0, 360)
        self.angular_velocity = random.uniform(-2, 2)
        scaled = Point(target.x - self.x,
                       target.y - self.y).set_magnitude(Thing.SPEED)
        self.dx, self.dy = scaled.x, scaled.y
        self.is_enemy = True

    def hit(self):
        # TODO: angle towards nearest enemy
        self.dx *= -1
        self.is_enemy = False
