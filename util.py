import os
from thing import *


def clamp(val, low, high):
    return max(low, min(high, val))


def load_from_path(path, load):
    assets = []
    for dir_name, dir_names, file_names in os.walk(path):
        for file_name in file_names:
            if file_name.endswith(".txt"):
                continue
            assets.append(load(os.path.join(dir_name, file_name)))
    return assets


def load_sounds_from_folder(folder):
    def load_sound(path):
        return pygame.mixer.Sound(path)
    return load_from_path("sounds/" + folder, load_sound)


def load_things_from_folder(folder):
    def load_thing(path):
        return Thing(pygame.image.load(path))
    return load_from_path("images/" + folder, load_thing)