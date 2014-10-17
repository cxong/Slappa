from game_object_factory import *
from scale_manager import *
from state import *
from world import *


class Game(object):
    def __init__(self, caption, width, height):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.init()
        pygame.display.set_caption(caption)
        self.width = width
        self.height = height

        self.add = GameObjectFactory(self)
        self.scale = ScaleManager(self)
        self.state = StateManager(self)
        self.world = World()

    def __exit__(self, type, value, traceback):
        pygame.mixer.quit()
        pygame.quit()