import pygame


class Sprite(object):
    def __init__(self, image, dimensions):
        self.image = image

        self.width = dimensions[0]
        self.height = dimensions[1]

        self.dx = 0
        self.dy = 0
        self.x = 0
        self.y = 0

        self.health = 0

        self.anchor = pygame.math.Vector2(0.5, 0.5)

    def update(self, time):
        self.x += self.dx * time
        self.y += self.dy * time

    def draw(self, surface):
       surface.blit(self.image,
                    self.x - self.width * self.anchor.x,
                    self.y - self.height * self.anchor.y)