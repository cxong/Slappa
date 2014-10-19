from simple_character import *
from util import *


class PlayerHurtBox(Sprite):
    def __init__(self, game, dx, dy, dimensions, player):
        super(PlayerHurtBox, self).__init__(
            game,
            player.x + player.body.x + dx,
            player.y + player.body.y + dy,
            '')
        self.dx = dx
        self.dy = dy
        self.body.width = dimensions[0]
        self.body.height = dimensions[1]
        self.count = player.hit_duration
        self.has_hit_monster = False
        self.player = player

    def update(self, time):
        self.count -= ANIM_FRAME_RATE / FRAME_RATE
        self.x = self.player.x + self.player.body.x + self.dx
        self.y = self.player.y + self.player.body.y + self.dy
        if self.count <= 0:
            self.health = 0


class Player(SimpleCharacter):
    def __init__(self, game, x, y, key, hurt_boxes):
        super(Player, self).__init__(game, x, y, key, (64, 64))

        self.animations.animations['idle'] = Animation([0, 1, 2, 3], 5, True)
        self.animations.animations['walk'] = Animation([16, 17, 18, 19, 20, 21, 22, 23], 2, True)
        self.animations.animations['jump'] = Animation([33, 34, 35, 34, 35, 34, 35, 36, 37], 5)
        self.animations.animations['hit'] = Animation(
            [144, 145, 146, 147, 148, 149, 149, 149, 149, 149, 149, 149, 150, 150, 150, 150], 1)
        self.animations.animations['hit_up'] = Animation(
            [128, 129, 130, 131, 132, 132, 133, 133, 134, 134, 135, 136, 137, 138, 139, 140], 1)
        self.animations.animations['hurt'] = Animation([65, 66, 65], 5)
        self.animations.animations['die'] = Animation([65, 66, 67, 68, 69, 70], 7)

        self.hit_duration = 5
        if key == 'cat':
            self.init_cat()
        elif key == 'dog':
            self.init_dog()

        self.anchor.y = 0.84
        self.body.y = -25
        self.body.width = self.width * 0.05
        self.body.height = self.height * 0.05

        self.health = 5
        self.out_of_bounds_kill = False

        self.sounds['jump'] = assets.sounds['jump']
        self.sounds['land'] = assets.sounds['land']
        self.sounds['swings'] = assets.sounds['swings']

        self.hurt_boxes = hurt_boxes

    def init_cat(self):
        self.speed = 0.3
        self.max_speed = 0.22
        self.gravity = 0.00198
        self.jump_force = 0.7

        self.sounds['hurts'] = [assets.sounds['meow']]
        self.sounds['deaths'] = [assets.sounds['meow']]

    def init_dog(self):
        self.animations.animations['idle'].duration = 6
        self.animations.animations['walk'].duration = 3
        self.animations.animations['jump'].duration = 7
        self.animations.animations['hit'] = Animation(
            [144, 145, 146, 147, 148, 149, 149, 149, 149, 149, 149, 149, 149, 149, 149, 149, 149, 149, 149, 150, 150, 150], 1)
        self.animations.animations['hit_up'] = Animation(
            [128, 129, 130, 131, 132, 132, 133, 133, 133, 133, 134, 134, 134, 134, 135, 135, 135, 136, 137, 138, 139, 140], 1)

        self.speed = 0.25
        self.max_speed = 0.18
        self.gravity = 0.0013
        self.jump_force = 0.6
        self.friction = 0.0005
        self.hit_duration = 12

        self.sounds['hurts'] = [assets.sounds['yelp']]
        self.sounds['deaths'] = [assets.sounds['yelp']]

    def exists(self):
        # Players always exist
        return True

    def update(self, time):
        super(Player, self).update(time)
        # Keep inside world
        self.x = max([self.x, self.width / 2])
        self.x = min([self.x, self.game.width - self.width / 2])
        self.y = max([self.y, self.height / 2])
        self.y = min([self.y, self.game.height - self.height / 2])

    def do_hit(self, direction):
        if direction == "left":
            self.hurt_boxes.add(PlayerHurtBox(self.game,
                                              -32,
                                              0,
                                              (64, 80),
                                              self))
        elif direction == "right":
            self.hurt_boxes.add(PlayerHurtBox(self.game,
                                              32,
                                              0,
                                              (64, 80),
                                              self))
        elif direction == "up":
            self.hurt_boxes.add(PlayerHurtBox(self.game,
                                              0,
                                              -32,
                                              (90, 64),
                                              self))
        super(Player, self).do_hit(direction)

    def draw(self, surface):
        super(Player, self).draw(surface)
