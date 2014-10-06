import pygame


class Keyboard:
    def __init__(self):
        self.keys = None

    def update(self):
        self.keys = pygame.key.get_pressed()

    def is_escape(self):
        return self.keys[pygame.K_ESCAPE]

    def dir(self):
        if self.keys[pygame.K_LEFT]:
            return -1
        elif self.keys[pygame.K_RIGHT]:
            return 1
        return 0

    def is_jump(self):
        return self.keys[pygame.K_UP]

    def hit(self):
        if self.keys[pygame.K_a]:
            return "left"
        elif self.keys[pygame.K_d]:
            return "right"
        elif self.keys[pygame.K_w]:
            return "up"
        return ""