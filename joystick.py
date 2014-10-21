import os
import platform
import pygame
import sys


class Joystick(object):
    def __init__(self, game):
        self.game = game
        self.joystick = None
        self.detect_period = 300
        self.detect_joystick()
        self._dir = 0
        self._is_jump = False
        self._hit = ""
        self.num_joystics = 0
        if platform.system() == 'Windows':
            # Workaround for stupid pygame leaving debug in
            sys.stdout = os.devnull
            sys.stderr = os.devnull

    def detect_joystick(self):
        self.detect_period = 300
        pygame.joystick.init()
        for i in range(pygame.joystick.get_count()):
            # Find compatible joystick
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            if (joystick.get_numbuttons() >= 4 and
                    (joystick.get_numaxes() >= 2 or
                     joystick.get_numhats() > 0)):
                self.num_joystics += 1
                # GCW Zero uses joystick 1 for its analog
                # Ignore it
                # TODO: use GCW Zero analog
                if not self.game.config.GCW_ZERO or self.num_joystics > 1:
                    self.joystick = joystick

    def update(self):
        self._dir = 0
        self._is_jump = False
        self._hit = ""
        if self.joystick is None:
            self.detect_period -= 1
            if self.detect_period == 0:
                self.detect_joystick()
        else:
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