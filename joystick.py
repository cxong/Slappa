import os
import platform
import sys
from config import *


class Joystick(object):
    def __init__(self, joystick):
        self.joystick = joystick
        self._dir = 0
        self._is_jump = False
        self._hit = ""

    def update(self):
        self._dir = 0
        self._is_jump = False
        self._hit = ""
        if self.joystick is None:
            return
        # Directions
        for i in range(self.joystick.get_numhats()):
            hat = self.joystick.get_hat(i)
            if self._dir == 0:
                self._dir = hat[0]
            if not self._is_jump:
                self._is_jump = hat[1] == 1
        for i in range(self.joystick.get_numaxes()):
            axis = self.joystick.get_axis(i)
            if abs(axis) > 0.3:
                if (i % 2) == 0:
                    if self._dir == 0:
                        self._dir = axis / abs(axis)
                elif (i % 2) == 1:
                    if not self._is_jump:
                        self._is_jump = axis < 0
        # Buttons
        if self.joystick.get_button(1) == 1:
            self._hit = "right"
        if self.joystick.get_button(2) == 1:
            self._hit = "left"
        if self.joystick.get_button(3) == 1:
            self._hit = "up"

    def dir(self):
        return self._dir

    def is_jump(self):
        return self._is_jump

    def hit(self):
        return self._hit

    def pressed(self):
        return self.dir() != 0 or self.is_jump() or self.hit() != ""


class Joysticks(object):
    def __init__(self):
        self.joysticks = []
        self.detect_period = 300
        self.detect_joystick()
        if platform.system() == 'Windows':
            # Workaround for stupid pygame leaving debug in
            sys.stdout = os.devnull
            sys.stderr = os.devnull

    def detect_joystick(self):
        self.detect_period = 300
        pygame.joystick.init()
        self.joysticks = []
        for i in range(pygame.joystick.get_count()):
            # Find compatible joystick
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            if (joystick.get_numbuttons() >= 4 and
                    (joystick.get_numaxes() >= 2 or
                     joystick.get_numhats() > 0)):
                self.joysticks.append(Joystick(joystick))
        # GCW Zero uses joystick 1 for its analog
        # Ignore it
        # TODO: use GCW Zero analog
        if GCW_ZERO and len(self.joysticks) > 0:
            del self.joysticks[0]

    def update(self):
        for joystick in self.joysticks:
            joystick.update()

    def __getitem__(self, item):
        if item >= len(self.joysticks):
            return None
        return self.joysticks[item]

    def __len__(self):
        return len(self.joysticks)