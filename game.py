from game_object_factory import *
from game_time import *
from loader import *
from scale_manager import *
from state import *
from world import *


class Game(object):
    def __init__(self, caption, width, height):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
        pygame.init()
        pygame.display.set_caption(caption)
        self.width = width
        self.height = height

        self.add = GameObjectFactory(self)
        self.config = Config()
        self.load = Loader()
        self.scale = ScaleManager(self)
        self.state = StateManager(self)
        self.time = Time()
        self.world = World()
        if GCW_ZERO:
            pygame.mouse.set_visible(False)

    def __exit__(self, type, value, traceback):
        pygame.mixer.quit()
        pygame.quit()
