from util import *


class SimpleCharacter(Sprite):
    def __init__(self, x, y, key, dimensions):
        rect = pygame.Rect(0, 0, dimensions[0], dimensions[1])
        super(SimpleCharacter, self).__init__(x, y,
                                              key,
                                              Point(2, 2),
                                              rect)

        self.animations.animations['idle'] = Animation([], 1, True)
        self.animations.animations['walk'] = Animation([], 1, True)
        self.animations.animations['hit'] = Animation([], 1)
        self.animations.animations['hit_up'] = Animation([], 1)
        self.animations.animations['hurt'] = Animation([], 1)
        self.animations.animations['die'] = Animation([], 1)
        self.animations.animations['jump'] = Animation([], 1)

        self.is_hitting = False
        self.is_hurt = False
        self.is_dying = False
        self.is_facing_right = True
        self.is_jumping = True
        self.speed = 0.1
        self.max_speed = 0.05
        self.jump_force = 0.0
        self.friction = 0.002

        self.sounds = {
            'swings': [],
            'hurts': [],
            'deaths': [],
            'land': None,
            'jump': None
        }

    def update(self, time):
        super(SimpleCharacter, self).update(time)

        if self.health > 0:
            self.is_dying = False
            if self.animations.animation_playing is None:
                self.animations.play('idle')

            # Friction, only on ground
            if self.is_on_ground() or self.gravity == 0.0:
                if self.dx > 0:
                    if not self.is_hitting and not self.is_hurt:
                        self.animations.play('walk')
                    self.dx = max(0, self.dx - self.friction * time)
                elif self.dx < 0:
                    if not self.is_hitting and not self.is_hurt:
                        self.animations.play('walk')
                    self.dx = min(0, self.dx + self.friction * time)
                else:
                    if not self.is_hitting and not self.is_hurt:
                        self.animations.play('idle')
            # Facing
            if not self.is_hitting:
                if self.dx > 0:
                    self.is_facing_right = True
                elif self.dx < 0:
                    self.is_facing_right = False
        else:
            self.dx = 0

    def land(self):
        self.y = FLOOR_Y
        if self.health > 0:
            if self.is_jumping:
                if self.sounds['land'] is not None:
                    self.sounds['land'].play()
                self.dx = 0
                self.dy = 0
                self.is_jumping = False
                if not self.is_hitting:
                    self.animations.play('idle')

    def hit(self, direction):
        if self.health <= 0:
            return
        if self.is_hitting:
            # We are already hitting; ignore
            return

        if direction == "left":
            self.is_facing_right = False
            self.animations.play('hit')
            self.do_hit(direction)
        elif direction == "right":
            self.is_facing_right = True
            self.animations.play('hit')
            self.do_hit(direction)
        elif direction == "up":
            self.animations.play('hit_up')
            self.do_hit(direction)

    def do_hit(self, direction):
        self.is_hitting = True
        random.choice(self.sounds['swings']).play()

        def after_hit(s):
            s.is_hitting = False
        self.animations.animation_playing.on_complete = [(after_hit, self)]

    def jump(self):
        # Can't jump if no gravity
        if self.gravity == 0.0:
            return
        # Can't move when dead
        if self.health <= 0:
            return

        if not self.is_on_ground():
            return
        self.is_jumping = True
        self.dy = -self.jump_force
        if self.sounds['jump'] is not None:
            self.sounds['jump'].play()
        self.animations.play('jump')

    def move(self, dx):
        # Can't move when dead
        if self.health <= 0:
            return

        # Can't move when attacking and on ground
        if self.is_hitting and self.is_on_ground():
            return
        self.dx += dx * self.speed
        self.dx = clamp(self.dx, -self.max_speed, self.max_speed)

    def is_on_ground(self):
        return self.y >= FLOOR_Y

    def exists(self):
        return self.is_dying or super(SimpleCharacter, self).exists()

    def hurt(self):
        if self.health <= 0:
            return False

        self.health -= 1

        if self.health > 0:
            random.choice(self.sounds['hurts']).play()
            self.is_hurt = True

            self.animations.play('hurt')

            def after_hurt(s):
                s.is_hurt = False
            self.animations.animation_playing.on_complete = [(after_hurt, self)]
        elif not self.is_dying:
            # Dead
            random.choice(self.sounds['deaths']).play()

            self.is_dying = True

            self.animations.play('die')

            def after_die(s):
                s.is_dying = False
            self.animations.animation_playing.on_complete = [(after_die, self)]

        return True

    def draw(self, surface):
        # Directional flip
        self.flip_x = not self.is_facing_right
        super(SimpleCharacter, self).draw(surface)