import pygame


class Loader(object):
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}

    def audio(self, key, path):
        if key not in self.sounds:
            self.sounds[key] = pygame.mixer.Sound(path)

    def font(self, key, path, size):
        if key not in self.fonts:
            self.fonts[key] = pygame.font.Font(path, size)

    def image(self, key, path):
        if key not in self.images:
            self.images[key] = pygame.image.load(path)#.convert()