from state import *


class Game(object):
    def __init__(self, caption, width, height):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.init()
        pygame.display.set_caption(caption)
        screen = pygame.display.set_mode([width, height])
        self.width = width
        self.height = height

        self.state = StateManager(self, screen)

    def __exit__(self, type, value, traceback):
        pygame.mixer.quit()
        pygame.quit()