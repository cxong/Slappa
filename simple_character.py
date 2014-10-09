import random
from config import *
from util import *


class SimpleCharacter(Sprite):
    def __init__(self, image_path, dimensions):
        rect = pygame.Rect(0, 0, dimensions[0], dimensions[1])
        super(SimpleCharacter, self).__init__(pygame.image.load(image_path),
                                              Point(2, 2),
                                              rect)

        self.animations.animations['idle'] = Animation([], 1, True)
        self.animations.animations['walk'] = Animation([], 1, True)
        self.animations.animations['die'] = Animation([], 1, True)

        self.is_hitting = False
        self.hit_duration = 15
        self.hit_counter = 0
        self.is_facing_right = True
        self.speed = 0.1
        self.max_speed = 0.05

        self.sounds = {
            'swings': [],
            'deaths': []
        }

    def update(self, time):
        super(SimpleCharacter, self).update(time)
        if self.animations.animation_playing is None:
            self.animations.play('idle')

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

    def hit(self, direction):
        if self.is_hitting:
            # We are already hitting; ignore
            return
        if direction == "left":
            self.is_facing_right = False
            self.animations.play('hit')
            self.do_hit(direction)
        elif direction == "right":
            self.is_facing_right = True
            self.animations.play('hit')
            self.do_hit(direction)
        elif direction == "up":
            self.animations.play('hit_up')
            self.do_hit(direction)

    def do_hit(self, direction):
        self.hit_counter = self.hit_duration
        self.is_hitting = True
        random.choice(self.sounds['swings']).play()

    def move(self, dx):
        # Can't move when attacking and on ground
        if self.is_hitting and self.is_on_ground():
            return
        self.dx += dx * self.speed
        self.dx = clamp(self.dx, -self.max_speed, self.max_speed)

    def is_on_ground(self):
        return self.y >= FLOOR_Y

    def draw(self, surface):
        # Directional flip
        self.flip_x = not self.is_facing_right
        super(SimpleCharacter, self).draw(surface)