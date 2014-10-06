from point import *


class Sprite(object):
    def __init__(self, image):
        self.image = image

        self.width = image.get_width()
        self.height = image.get_height()

        self.dx = 0
        self.dy = 0
        self.x = 0
        self.y = 0

        self.health = 0

        self.anchor = Point(0.5, 0.5)

    def update(self, time):
        self.x += self.dx * time
        self.y += self.dy * time

    def draw(self, surface):
       surface.blit(self.image,
                    (self.x - self.width * self.anchor.x,
                    self.y - self.height * self.anchor.y))