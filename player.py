import pygame
from config import *
from simple_character import *
from util import *


class Player(SimpleCharacter):
    GRAVITY = 0.00198
    SPEED = 0.3
    MAX_SPEED = 0.2
    JUMP_FORCE = 0.7

    def __init__(self, image_path, dimensions):
        super(Player, self).__init__(image_path, dimensions)

        self.x = SCREEN_SIZE[0] / 2
        self.y = FLOOR_Y
        self.anchor.y = 0.34

        self.animations.animations['idle'] = Animation([0, 1, 2, 3], 5, True)
        self.animations.animations['walk'] = Animation([16, 17, 18, 19, 20, 21, 22, 23], 2, True)
        self.animations.animations['jump'] = Animation([33, 34, 35, 34, 35, 34, 35, 36, 37], 5)
        self.animations.animations['hit'] = Animation([144, 145, 146, 147, 148, 149, 149, 149, 149, 150], 1)
        self.animations.animations['hit_up'] = Animation([128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140], 1)
        self.animations.animations['die'] = Animation([65, 66, 67, 68, 69, 70], 5)

        self.is_jumping = True
        self.hit_duration = 15
        self.speed = Player.SPEED
        self.max_speed = Player.MAX_SPEED

        self.sounds = {
            'jump': pygame.mixer.Sound("sounds/jump.ogg"),
            'land': pygame.mixer.Sound("sounds/land.ogg"),
            'swings': load_sounds_from_folder("swings"),
            'deaths': [pygame.mixer.Sound("sounds/meow.ogg")]
        }

    def update(self, time):
        self.dy += Player.GRAVITY * time
        super(Player, self).update(time)
        if self.y > FLOOR_Y:
            self.land()

    def land(self):
        self.y = FLOOR_Y
        if self.is_jumping:
            self.sounds['land'].play()
            self.dx = 0
            self.dy = 0
            self.is_jumping = False
            if not self.is_hitting:
                self.animations.play('idle')
                pass

    def hit(self, direction):
        if self.is_hitting:
            # We are already hitting; ignore
            return
        if direction == "left":
            # TODO: hit
            pass
        elif direction == "right":
            # TODO: hit
            pass
        elif direction == "up":
            # TODO: hit
            pass
        super(Player, self).hit(direction)

    def jump(self):
        if not self.is_on_ground():
            return
        self.is_jumping = True
        self.dy = -Player.JUMP_FORCE
        self.sounds['jump'].play()
        self.animations.play('jump')

    def draw(self, surface):
        super(Player, self).draw(surface)
