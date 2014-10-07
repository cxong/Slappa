import pygame
from config import *
from sprite import *
from util import *

GRAVITY = 0.00198
SPEED = 0.3
MAX_SPEED = 0.2
JUMP_FORCE = 0.7
FRICTION = 0.002


class Player(Sprite):
    def __init__(self, image_path, dimensions):
        rect = pygame.Rect(0, 0, dimensions[0], dimensions[1])
        super(Player, self).__init__(pygame.image.load(image_path),
                                     Point(2, 2),
                                     rect)
        self.x = SCREEN_SIZE[0] / 2
        self.y = FLOOR_Y
        self.anchor.y = 0.34

        self.animations.animations['idle'] = Animation([0, 1, 2, 3], 5, True)
        self.animations.play('idle')

        self.is_jumping = True
        self.is_hitting = False
        self.is_facing_right = True

        self.sounds = {
            'jump': pygame.mixer.Sound("sounds/jump.ogg"),
            'land': pygame.mixer.Sound("sounds/land.ogg")
        }

    def update(self, time):
        self.dy += GRAVITY * time
        super(Player, self).update(time)
        if self.y > FLOOR_Y:
            self.land()
        # Friction, only on ground
        if self.is_on_ground():
            if self.dx > 0:
                self.dx = max(0, self.dx - FRICTION * time)
            elif self.dx < 0:
                self.dx = min(0, self.dx + FRICTION * time)
        # Facing
        if self.dx > 0:
            self.is_facing_right = True
        elif self.dx < 0:
            self.is_facing_right = False

    def land(self):
        self.y = FLOOR_Y
        if self.is_jumping:
            self.sounds['land'].play()
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
        self.dy = -JUMP_FORCE
        self.sounds['jump'].play()
        # TODO: switch to jump sprite

    def is_on_ground(self):
        return self.y >= FLOOR_Y

    def draw(self, surface):
        # Directional flip
        self.flip_x = not self.is_facing_right
        super(Player, self).draw(surface)