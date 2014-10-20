import pygame


class Time:
    def __init__(self):
        self.advanced_timing = False
        self.clock = pygame.time.Clock()
        self.fps = 0

    def update(self, time):
        if self.advanced_timing:
            self.fps = self.clock.get_fps()