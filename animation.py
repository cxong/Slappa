import pygame

class Animation(object):
    def __init__(self, frames, duration=1, loop=False):
        self.frames = frames
        self.duration = duration
        self.loop = loop

        self.counter = -1

    def update(self):
        self.counter += 1
        if self.counter == len(self.frames):
            self.counter = 0

    def get_crop(self, dimensions, image_width):
        frame = self.frames[self.counter]
        x = frame * dimensions[0]
        y = 0
        while x + dimensions[0] >= image_width:
            x -= image_width
            y += dimensions[1]
        return pygame.Rect(x, y, dimensions[0], dimensions[1])

class AnimationManager(object):
    def __init__(self):
        self.animations = {}
        self.animation_playing = None

    def play(self, name):
        self.animation_playing = self.animations[name]

    def update(self):
        if self.animation_playing is not None:
            self.animation_playing.update()

    def get_crop(self, dimensions, image_width):
        if self.animation_playing is None:
            return pygame.Rect(0, 0, dimensions[0], dimensions[1])
        return self.animation_playing.get_crop(dimensions, image_width)