import pygame
from config import *


class Animation(object):
    def __init__(self, game, frames, duration=1, loop=False):
        self.game = game
        self.frames = frames[:]
        self.duration = duration
        self.loop = loop
        self.is_playing = False
        self.on_complete = []

        self.counter = 0
        self.sub_counter = 0

    def reset(self):
        self.counter = -1
        self.sub_counter = 0

    def play(self):
        if self.is_playing:
            return
        self.reset()
        self.is_playing = True

    def update(self):
        if not self.is_playing:
            return
        self.sub_counter += self.game.config.ANIM_FRAME_RATE / self.game.config.FRAME_RATE
        while self.sub_counter >= self.duration:
            self.sub_counter -= self.duration
            self.counter += 1
        if self.counter >= len(self.frames):
            if self.loop:
                self.counter = 0
            else:
                self.complete()

    def complete(self):
        self.reset()
        self.is_playing = False
        for (func, data) in self.on_complete:
            func(data)
        self.on_complete = []

    def get_crop(self, dimensions, image_width):
        frame = self.frames[self.counter]
        x = frame * dimensions[0]
        y = 0
        while x + dimensions[0] > image_width:
            x -= image_width
            y += dimensions[1]
        return pygame.Rect(x, y, dimensions[0], dimensions[1])


class AnimationManager(object):
    def __init__(self):
        self.animations = {}
        self.animation_playing = None

    def play(self, name):
        if (self.animation_playing == self.animations[name] and
                self.animation_playing.is_playing):
            return
        # Stop the last animation
        if self.animation_playing is not None:
            self.animation_playing.complete()
        self.animation_playing = self.animations[name]
        self.animation_playing.play()

    def update(self):
        if self.animation_playing is not None:
            self.animation_playing.update()

    def get_crop(self, dimensions, image_width):
        if self.animation_playing is None:
            return pygame.Rect(0, 0, dimensions[0], dimensions[1])
        return self.animation_playing.get_crop(dimensions, image_width)