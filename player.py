import pygame
from config import *
from sprite import *
from util import *

GRAVITY = 0.00198
SPEED = 0.03
MAX_SPEED = 0.2
JUMP_FORCE = 0.7
FRICTION = 0.05


class Player(Sprite):
    def __init__(self, image_path, dimensions):
        rect = pygame.Rect(0, 0, dimensions[0], dimensions[1])
        image = pygame.Surface(rect.size).convert()
        image.blit(pygame.image.load(image_path).convert(), (0, 0), rect)
        super(Player, self).__init__(image, dimensions)

        self.is_jumping = True
        self.is_hitting = False

    def update(self, time):
        self.dy += GRAVITY * time
        super(Player, self).update(time)
        if self.y > FLOOR_Y:
            self.y = FLOOR_Y
            self.land()
        if self.dx > 0:
            self.dx = max(0, self.dx - FRICTION)
        else:
            self.dx = min(0, self.dx + FRICTION)

    def land(self):
        if self.is_jumping:
            self.dx = 0
            self.dy = 0
            self.is_jumping = False
            if not self.is_hitting:
                # TODO: switch to idle sprite here
                pass

    def hit(self, direction):
        self.is_hitting = True
        if direction == "left":
            # TODO: hit
            pass
        elif direction == "right":
            # TODO: hit
            pass
        elif direction == "up":
            # TODO: hit
            pass

    def move(self, dx):
        self.dx += dx * SPEED
        self.dx = clamp(self.dx, -MAX_SPEED, MAX_SPEED)

    def jump(self):
        if not self.is_on_ground():
            return
        self.is_jumping = True
        self.dy -= JUMP_FORCE
        # TODO: switch to jump sprite

    def is_on_ground(self):
        return self.y <= FLOOR_Y

    def draw(self, surface):
        # TODO: boxes
        super(Player, self).draw(surface)