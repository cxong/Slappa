import pygame
from config import *


class StateManager(object):
    def __init__(self, game):
        self.states = {}
        self.screen = None  # Lazy initialise
        self.game = game
        self.active_state = None

    def add(self, key, state):
        self.states[key] = state
        state.state = self
        state.game = self.game

    def start(self, key):
        if self.active_state is not None:
            # We want to start a new state
            # Just tell the current one to stop
            self.active_state.is_quit = True
            self.active_state = self.states[key]
            return
        if self.active_state is None:
            # First time
            self.active_state = self.states[key]
        while True:
            state = self.active_state
            if self.screen is None:
                self.screen = pygame.display.set_mode([self.game.scale.width,
                                                       self.game.scale.height])
            state.start(self.screen)
            # At this stage, we either want to quit or we're changing to a new
            # state
            if state == self.active_state and state.is_quit:
                break


class State(object):
    def __init__(self):
        self.preload = None
        self.create = None
        self.update = None
        self.draw = None
        self.started = False
        self.is_quit = False
        self.state = None
        self.game = None

    def start(self, screen):
        self.started = True
        self.is_quit = False
        screen_buf = pygame.Surface([self.game.width, self.game.height])
        final_buf = screen_buf
        if (self.game.width != self.game.scale.width or
                self.game.height != self.game.scale.height):
            final_buf = pygame.Surface([self.game.scale.width,
                                        self.game.scale.height])
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
                elif event.type == pygame.KEYDOWN:
                    if self.game.keys.on_down is not None:
                        self.game.keys.on_down(event.key, event.unicode)

            self.game.world.update(clock.get_time())
            if self.update is not None:
                self.update(clock.get_time())
            self.game.world.draw(screen_buf)
            if self.draw is not None:
                self.draw(screen_buf)
            # Final scaling
            if (self.game.width != self.game.scale.width or
                    self.game.height != self.game.scale.height):
                pygame.transform.scale(
                    screen_buf,
                    (self.game.scale.width, self.game.scale.height),
                    final_buf)
            screen.blit(final_buf, (0, 0))
            pygame.display.flip()
            clock.tick(FRAME_RATE)
        # Remove all stuff from stage
        self.game.world.destroy()
        self.started = False