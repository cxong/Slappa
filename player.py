from simple_character import *
from util import *


class PlayerHurtBox(Sprite):
    def __init__(self, x, y, dimensions):
        super(PlayerHurtBox, self).__init__(x, y, '')
        self.body.width = dimensions[0]
        self.body.height = dimensions[1]
        self.count = 5
        self.has_hit_monster = False

    def update(self, time):
        self.count -= 1
        if self.count <= 0:
            self.health = 0


class Player(SimpleCharacter):
    GRAVITY = 0.00198
    SPEED = 0.3
    MAX_SPEED = 0.2
    JUMP_FORCE = 0.7

    def __init__(self, x, y, key, dimensions, hurt_boxes):
        super(Player, self).__init__(x, y, key, dimensions)

        self.anchor.y = 0.84
        self.body.y = -25
        self.body.width = self.width * 0.05
        self.body.height = self.height * 0.05

        self.animations.animations['idle'] = Animation([0, 1, 2, 3], 5, True)
        self.animations.animations['walk'] = Animation([16, 17, 18, 19, 20, 21, 22, 23], 2, True)
        self.animations.animations['jump'] = Animation([33, 34, 35, 34, 35, 34, 35, 36, 37], 5)
        self.animations.animations['hit'] = Animation([144, 145, 146, 147, 148, 149, 149, 149, 149, 150, 150, 150, 150], 1)
        self.animations.animations['hit_up'] = Animation([128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140], 1)
        self.animations.animations['hurt'] = Animation([65, 66, 65], 5)
        self.animations.animations['die'] = Animation([65, 66, 67, 68, 69, 70], 7)

        self.is_jumping = True
        self.speed = Player.SPEED
        self.max_speed = Player.MAX_SPEED
        self.health = 5
        self.out_of_bounds_kill = False

        self.sounds = {
            'jump': assets.sounds['jump'],
            'land': assets.sounds['land'],
            'swings': assets.sounds['swings'],
            'hurts': [assets.sounds['meow']],
            'deaths': [assets.sounds['meow']]
        }

        self.hurt_boxes = hurt_boxes

    def update(self, time):
        self.dy += Player.GRAVITY * time
        super(Player, self).update(time)
        if self.y > FLOOR_Y:
            self.land()
        # Keep inside world
        self.x = max([self.x, self.width / 2])
        self.x = min([self.x, SCREEN_SIZE[0] - self.width / 2])
        self.y = max([self.y, self.height / 2])
        self.y = min([self.y, SCREEN_SIZE[1] - self.height / 2])

    def land(self):
        self.y = FLOOR_Y
        if self.health > 0:
            if self.is_jumping:
                self.sounds['land'].play()
                self.dx = 0
                self.dy = 0
                self.is_jumping = False
                if not self.is_hitting:
                    self.animations.play('idle')
                    pass

    def do_hit(self, direction):
        if direction == "left":
            self.hurt_boxes.add(PlayerHurtBox(self.x - 32,
                                              self.y + self.body.y,
                                              (64, 80)))
        elif direction == "right":
            self.hurt_boxes.add(PlayerHurtBox(self.x + 32,
                                              self.y + self.body.y,
                                              (64, 80)))
        elif direction == "up":
            self.hurt_boxes.add(PlayerHurtBox(self.x,
                                              self.y + self.body.y - 32,
                                              (90, 64)))
        super(Player, self).do_hit(direction)

    def jump(self):
        # Can't move when dead
        if self.health <= 0:
            return

        if not self.is_on_ground():
            return
        self.is_jumping = True
        self.dy = -Player.JUMP_FORCE
        self.sounds['jump'].play()
        self.animations.play('jump')

    def draw(self, surface):
        super(Player, self).draw(surface)
