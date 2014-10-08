from simple_character import *


class Enemy(SimpleCharacter):
    SPEED = 0.1
    MAX_SPEED = 0.05

    def __init__(self, image_path, dimensions):
        super(Enemy, self).__init__(image_path, dimensions)

        self.anchor.y = 0.34

        self.animations.animations['idle'] = Animation([0, 1, 2, 3], 20, True)
        self.animations.animations['walk'] = Animation([8, 9, 10, 11, 12], 20, True)
        self.animations.animations['hit'] = Animation([16, 17, 18, 19, 20, 21], 1)
        self.animations.animations['die'] = Animation([25, 26, 27, 28, 29, 30], 20)

        self.hit_duration = 50
        self.speed = Enemy.SPEED
        self.max_speed = Enemy.MAX_SPEED

        self.sounds = {
            'swings': load_sounds_from_folder("growls"),
            'deaths': load_sounds_from_folder("deaths")
        }

        # Random behaviour
        self.delay = 60
        self.action = 'idle'

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
                self.action = new_action
                break