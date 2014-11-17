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
                self.screen = pygame.display.set_mode(
                    [self.game.scale.width, self.game.scale.height],
                    pygame.DOUBLEBUF | pygame.HWSURFACE | self.game.config.SDL_FLAGS)
                pygame.mouse.set_visible(self.game.config.MOUSE_VISIBLE)
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
        if self.preload is not None:
            self.preload()
        if self.create is not None:
            self.create()
        clock = self.game.time.clock
        clock.tick()
        while not self.is_quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_quit = True
                elif event.type == pygame.KEYDOWN:
                    if self.game.keys.on_down is not None:
                        self.game.keys.on_down(event.key, event.unicode)
            # Don't update or draw if paused
            if not self.game.paused:
                self.game.world.update(clock.get_time())
                if self.update is not None:
                    self.update(clock.get_time())
                self.draw_screen(screen)
                clock.tick_busy_loop(self.game.config.FRAME_RATE)
            else:
                # Try less power hungry tick
                clock.tick(self.game.config.FRAME_RATE)
            self.game.time.update(clock.get_time())
        # Remove all stuff from stage
        self.game.world.destroy()
        # Clean up callbacks from last state
        self.game.on_paused = None
        self.game.on_resume = None
        self.started = False

    def draw_screen(self, screen):
        screen.fill((100, 149, 237))
        self.game.world.draw(screen)
        if self.draw is not None:
            self.draw(screen)
        pygame.display.flip()