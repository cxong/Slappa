from simple_character import *


class Enemy(SimpleCharacter):
    def __init__(self, x, y, key, players, thing_keys, things):
        if key == 'monster':
            self.init_monster(x, y)
        elif key == 'flying':
            self.init_flying(x, y)

        self.body.width = self.width * 0.5
        self.body.height = self.height * 0.5

        # Random behaviour
        self.delay = 60
        self.action = 'idle'

        self.players = players
        self.thing_key = random.choice(thing_keys)
        self.thing_group = things
        self.hit_offset = Point(0, -25)

        self.sounds = {
            'swings': assets.sounds['growls'],
            'hurts': assets.sounds['deaths'],
            'deaths': assets.sounds['deaths']
        }

    def init_monster(self, x, y):
        super(Enemy, self).__init__(x, y, 'monster', (64, 64))

        self.body.y = -25
        self.anchor.y = 0.84

        self.animations.animations['idle'] = Animation([0, 1, 2, 3], 20, True)
        self.animations.animations['walk'] = Animation([8, 9, 10, 11, 12], 20, True)
        self.animations.animations['hit'] = Animation([16, 17, 18, 19, 20, 21], 4)
        self.animations.animations['hurt'] = Animation([25, 26], 20)
        self.animations.animations['die'] = Animation([25, 26, 27, 28, 29, 30], 3)

        self.health = 2
        self.speed = 0.1
        self.max_speed = 0.05

    def init_flying(self, x, y):
        super(Enemy, self).__init__(x, y, 'flying', (64, 64))

        #self.anchor.y = 0.84

        self.animations.animations['idle'] = Animation([0, 1, 2, 3, 4], 10, True)
        self.animations.animations['walk'] = Animation([0, 1, 2, 3, 4], 10, True)
        self.animations.animations['hit'] = Animation([9, 10, 11, 12], 5)
        self.animations.animations['hurt'] = Animation([17, 18], 20)
        self.animations.animations['die'] = Animation([17, 18, 19, 20, 21, 22, 23], 3)

        self.health = 1
        self.speed = 0.2
        self.max_speed = 0.1

    def update(self, time):
        super(Enemy, self).update(time)
        if self.is_hitting:
            return
        self.delay -= 1
        # Perform the action
        if self.action == 'idle':
            # Idle; don't do anything
            pass
        elif self.action == 'hit':
            self.hit(random.choice(['left', 'right']))  # TODO: hit player
        elif self.action == 'move_left':
            self.move(-1)
        elif self.action == 'move_right':
            self.move(1)
        if self.delay == 0 or self.action == 'hit':
            self.delay = random.randint(40, 60)
            # Switch to new action
            while True:
                new_action = random.choice(['idle', 'hit', 'move_left', 'move_right'])
                # Reject impossible actions (need to place hits between idles)
                if self.action != 'idle' and new_action == 'hit':
                    continue
                if self.action == 'hit' and new_action != 'idle':
                    continue
                # Don't do same thing twice
                if self.action == new_action:
                    continue
                # Try to move towards center of screen
                if (new_action == 'move_left' and
                        self.x < SCREEN_SIZE[0] / 4):
                    continue
                if (new_action == 'move_right' and
                        self.x > SCREEN_SIZE[0] * 3 / 4):
                    continue
                self.action = new_action
                break

    def do_hit(self, direction):
        super(Enemy, self).do_hit(direction)
        # Throw a thing at a player
        self.thing_group.add(Thing(self.x + self.hit_offset.x,
                                   self.y + self.hit_offset.y,
                                   self.thing_key,
                                   random.choice(self.players.children).get_body_center()))
