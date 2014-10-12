import pygame
from config import *


class StateManager(object):
    def __init__(self, game, screen):
        self.states = {}
        self.screen = screen
        self.game = game
        self.active_state = None

    def add(self, key, state):
        self.states[key] = state
        state.state = self
        state.game = self.game

    def start(self, key):
        if self.active_state is not None:
            self.active_state.is_quit = True
        self.active_state = self.states[key]
        self.active_state.start(self.screen)


class State(object):
    def __init__(self):
        self.preload = None
        self.create = None
        self.update = None
        self.draw = None
        self.is_quit = False
        self.state = None
        self.game = None

    def start(self, screen):
        self.is_quit = False
        screenBuf = pygame.Surface(SCREEN_SIZE)
        if self.preload is not None:
            self.preload()
        if self.create is not None:
            self.create()
        clock = pygame.time.Clock()
        clock.tick()
        while not self.is_quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_quit = True

            if self.update is not None:
                self.update(clock.get_time())
            if self.draw is not None:
                self.draw(screenBuf)
                screen.blit(screenBuf, (0, 0))
                pygame.display.flip()
            clock.tick(FRAME_RATE)