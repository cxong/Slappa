from config import *


class Keyboard:
    def __init__(self):
        self.keys = None
        self.left = pygame.K_LEFT
        self.right = pygame.K_RIGHT
        self.jump = pygame.K_UP
        self.hit_left = pygame.K_a
        self.hit_right = pygame.K_d
        self.hit_up = pygame.K_w
        if GCW_ZERO:
            self.hit_left = pygame.K_LSHIFT
            self.hit_right = pygame.K_LCTRL
            self.hit_up = pygame.K_SPACE
        self.on_down = None

    def update(self):
        self.keys = pygame.key.get_pressed()

    def is_escape(self):
        return self.keys is not None and self.keys[pygame.K_ESCAPE]

    def dir(self):
        if self.keys is None:
            return 0
        if self.keys[self.left]:
            return -1
        elif self.keys[self.right]:
            return 1
        return 0

    def is_jump(self):
        return self.keys is not None and self.keys[self.jump]

    def hit(self):
        if self.keys is None:
            return ""
        if self.keys[self.hit_left]:
            return "left"
        elif self.keys[self.hit_right]:
            return "right"
        elif self.keys[self.hit_up]:
            return "up"
        return ""

    def pressed(self):
        return self.dir() != 0 or self.is_jump() or self.hit() != ""