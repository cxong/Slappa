import random
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
        self.animations.animations['walk'] = Animation([16, 17, 18, 19, 20, 21, 22, 23], 2, True)
        self.animations.animations['jump'] = Animation([33, 34, 35, 34, 35, 34, 35, 36, 37], 5)
        self.animations.animations['hit'] = Animation([144, 145, 146, 147, 148, 149, 149, 149, 149, 150], 1)
        self.animations.animations['hit_up'] = Animation([128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140], 1)
        self.animations.play('idle')

        self.is_jumping = True
        self.is_hitting = False
        self.hit_duration = 15
        self.hit_counter = 0
        self.is_facing_right = True

        self.sounds = {
            'jump': pygame.mixer.Sound("sounds/jump.ogg"),
            'land': pygame.mixer.Sound("sounds/land.ogg"),
            'swings': load_sounds_from_folder("swings")
        }

    def update(self, time):
        self.dy += GRAVITY * time
        super(Player, self).update(time)
        if self.y > FLOOR_Y:
            self.land()
        # Friction, only on ground
        if self.is_on_ground():
            if self.dx > 0:
                if not self.is_hitting:
                    self.animations.play('walk')
                self.dx = max(0, self.dx - FRICTION * time)
            elif self.dx < 0:
                if not self.is_hitting:
                    self.animations.play('walk')
                self.dx = min(0, self.dx + FRICTION * time)
            else:
                if not self.is_hitting:
                    self.animations.play('idle')
        # Facing
        if not self.is_hitting:
            if self.dx > 0:
                self.is_facing_right = True
            elif self.dx < 0:
                self.is_facing_right = False
        # Hitting
        if self.is_hitting:
            self.hit_counter -= 1
            if self.hit_counter == 0:
                self.is_hitting = False

    def land(self):
        self.y = FLOOR_Y
        if self.is_jumping:
            self.sounds['land'].play()
            self.dx = 0
            self.dy = 0
            self.is_jumping = False
            if not self.is_hitting:
                self.animations.play('idle')
                pass

    def hit(self, direction):
        if self.is_hitting:
            # We are already hitting; ignore
            return
        if direction == "left":
            # TODO: hit
            self.is_facing_right = False
            self.animations.play('hit')
            self.do_hit()
        elif direction == "right":
            # TODO: hit
            self.is_facing_right = True
            self.animations.play('hit')
            self.do_hit()
        elif direction == "up":
            # TODO: hit
            self.animations.play('hit_up')
            self.do_hit()

    def do_hit(self):
        self.hit_counter = self.hit_duration
        self.is_hitting = True
        random.choice(self.sounds['swings']).play()

    def move(self, dx):
        # Can't move when attacking and on ground
        if self.is_hitting and self.is_on_ground():
            return
        self.dx += dx * SPEED
        self.dx = clamp(self.dx, -MAX_SPEED, MAX_SPEED)

    def jump(self):
        if not self.is_on_ground():
            return
        self.is_jumping = True
        self.dy = -JUMP_FORCE
        self.sounds['jump'].play()
        self.animations.play('jump')

    def is_on_ground(self):
        return self.y >= FLOOR_Y

    def draw(self, surface):
        # Directional flip
        self.flip_x = not self.is_facing_right
        super(Player, self).draw(surface)