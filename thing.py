import random
from sprite import *


class Thing(Sprite):
    SPEED = 0.3

    def __init__(self, game, x, y, key, target):
        super(Thing, self).__init__(game, x, y, key)

        self.allow_rotations = True
        self.rotation = random.randint(0, 360)
        self.angular_velocity = random.uniform(-1, 1)
        scaled = Point(target.x - self.x,
                       target.y - self.y).set_magnitude(Thing.SPEED)
        self.dx, self.dy = scaled.x, scaled.y
        self.is_enemy = True

    def hit(self, player, enemies):
        self.angular_velocity = random.uniform(-2, 2)
        d = Point(self.x - (player.x + player.body.x),
                  self.y - (player.y + player.body.y)).normalize()
        # find enemies within arc of deflection
        in_arc_enemies = []
        for enemy in enemies:
            ed = Point(enemy.x - self.x, enemy.y - self.y)
            ed.normalize()
            half_angle = math.cos(
                math.radians(self.game.config.DEFLECTION_AUTOAIM_ANGLE / 2))
            if d.dot_product(ed) > half_angle:
                in_arc_enemies.append(enemy)
        # use closest enemy
        if len(in_arc_enemies) > 0:
            enemy = min(
                in_arc_enemies,
                key=lambda e: Point(e.x, e.y).distance2(
                    Point(self.x, self.y)))
            d = Point(enemy.x + enemy.body.x - self.x,
                      enemy.y + enemy.body.y - self.y).normalize()
        d.set_magnitude(Thing.SPEED * self.game.config.DEFLECTION_SPEED_SCALE)
        self.dx, self.dy = d.x, d.y
        self.is_enemy = False
