import random
from sprite import *


class Thing(Sprite):
    SPEED = 0.3

    def __init__(self, image_name):
        super(Thing, self).__init__(image_name)

        self.allow_rotations = True
        self.rotation = random.randint(0, 360)
        self.angular_velocity = 0

    def move_to(self, target):
        self.angular_velocity = random.uniform(-2, 2)
        scaled = Point(target.x - self.x,
                       target.y - self.y).set_magnitude(Thing.SPEED)
        self.dx, self.dy = scaled.x, scaled.y