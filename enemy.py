from simple_character import *


class Enemy(SimpleCharacter):
    def __init__(self, game, x, y, key, players, thing_keys, things):
        self.moves = True
        if key == 'zombie':
            self.init_zombie(game, x, y)
        elif key == 'monster':
            self.init_monster(game, x, y)
        elif key == 'flying':
            self.init_flying(game, x, y)

        self.body.width = self.width * 0.5
        self.body.height = self.height * 0.5

        # Random behaviour
        self.delay = 60
        self.action = 'idle'
        # Counter for throwing at a delay
        self.throw_counter = 0

        self.players = players
        self.thing_key = random.choice(thing_keys)
        self.thing_group = things
        self.hit_offset = Point(0, -25)

        self.sounds['swings'] = game.audio['growls']
        self.sounds['hurts'] = game.audio['deaths']
        self.sounds['deaths'] = game.audio['deaths']

    def init_zombie(self, game, x, y):
        super(Enemy, self).__init__(game, x, y, 'zombie', (64, 64))

        self.body.y = -35
        self.anchor.y = 0.95

        width = 4
        self.animations.animations['idle'] = Animation(game, [0, 1, 2, 3], 20, True)
        row = 1 * width
        self.animations.animations['walk'] = Animation(
            game, [row + x for x in [0, 1, 2, 3]], 20, True)
        row = 2 * width
        self.animations.animations['hit'] = Animation(
            game, [row + x for x in [1, 2, 3]], 7)
        row = 3 * width
        self.animations.animations['hurt'] = Animation(
            game, [row + x for x in [0, 1]], 20)
        self.animations.animations['die'] = Animation(
            game, [row + x for x in [0, 1, 2, 3]], 5)

        self.health = 2
        self.speed = 0.1
        self.max_speed = 0.05

    def init_monster(self, game, x, y):
        super(Enemy, self).__init__(game, x, y, 'monster', (64, 64))

        self.body.y = -25
        self.anchor.y = 0.84

        width = 4
        self.animations.animations['idle'] = Animation(game, [0, 1, 2, 3], 20, True)
        row = width * 1
        self.animations.animations['walk'] = Animation(
            game, [row + x for x in [0, 1, 2, 3]], 20, True)
        row = width * 4
        self.animations.animations['jump'] = Animation(
            game, [row + x for x in [0, 1, 2, 3, 2, 3, 2, 3]], 14)
        row = width * 2
        self.animations.animations['hit'] = Animation(
            game, [row + x for x in [0, 1, 2, 3, 0]], 4)
        row = width * 3
        self.animations.animations['hurt'] = Animation(
            game, [row + x for x in [0, 1]], 20)
        self.animations.animations['die'] = Animation(
            game, [row + x for x in [0, 1, 2, 3]], 5)

        self.health = 2
        self.speed = 0.1
        self.max_speed = 0.05
        self.gravity = 0.0003
        self.jump_force = 0.3
        self.moves = False

    def init_flying(self, game, x, y):
        super(Enemy, self).__init__(game, x, y, 'flying', (64, 64))

        width = 4
        self.animations.animations['idle'] = Animation(game, [0, 1, 2, 3], 12, True)
        self.animations.animations['walk'] = Animation(game, [0, 1, 2, 3], 10, True)
        row = width * 1
        self.animations.animations['hit'] = Animation(
            game, [row + x for x in [0, 1, 2, 3]], 5)
        row = width * 2
        self.animations.animations['hurt'] = Animation(
            game, [row + x for x in [0, 1]], 20)
        self.animations.animations['die'] = Animation(
            game, [row + x for x in [0, 1, 2, 3]], 5)

        self.health = 1
        self.speed = 0.2
        self.max_speed = 0.1

    def update(self, time):
        super(Enemy, self).update(time)
        if self.y > self.game.config.FLOOR_Y:
            self.y = self.game.config.FLOOR_Y
        if self.is_hitting:
            return
        self.delay -= self.game.config.ANIM_FRAME_RATE / self.game.config.FRAME_RATE
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
        elif self.action == 'jump_left':
            if not self.is_jumping:
                self.jump()
            self.move(-1)
        elif self.action == 'jump_right':
            if not self.is_jumping:
                self.jump()
            self.move(1)
        if self.delay <= 0 or self.action == 'hit':
            self.delay = random.randint(40, 60)
            # Switch to new action
            while True:
                new_action = random.choice([
                    'idle', 'hit', 'move_left', 'move_right',
                    'jump_left', 'jump_right'])
                # Reject impossible actions (need to place hits between idles)
                if self.action != 'idle' and new_action == 'hit':
                    continue
                if self.action == 'hit' and new_action != 'idle':
                    continue
                # Don't do same thing twice
                if self.action == new_action:
                    continue
                # Try to move towards center of screen
                if (new_action in ('move_left', 'jump_left') and
                        self.x < self.game.width / 4):
                    continue
                if (new_action in ('move_right', 'jump_right') and
                        self.x > self.game.width * 3 / 4):
                    continue
                # See if we can jump
                if self.gravity == 0.0 and (
                        new_action in ('jump_left', 'jump_right')):
                    continue
                # See if we can move
                if not self.moves and (
                        new_action in ('move_left', 'move_right')):
                    continue
                self.action = new_action
                break
        if self.throw_counter > 0:
            self.throw_counter -= time
            if self.throw_counter <= 0:
                self.throw()

    def do_hit(self, direction):
        players_alive = [p for p in self.players.children if p.health > 0]
        if len(players_alive) == 0:
            return
        super(Enemy, self).do_hit(direction)
        self.throw_counter = 70

    def throw(self):
        players_alive = [p for p in self.players.children if p.health > 0]
        if len(players_alive) == 0:
            return
        # Throw a thing at a player
        player = random.choice(players_alive)
        player_center = player.get_body_center()
        # Randomly offset target
        player_center.add(Point(
            random.uniform(-self.game.config.ENEMY_TARGET_OFFSET,
                           self.game.config.ENEMY_TARGET_OFFSET),
            random.uniform(-self.game.config.ENEMY_TARGET_OFFSET,
                           self.game.config.ENEMY_TARGET_OFFSET)))
        player_center.y = min([self.game.config.FLOOR_Y + player.body.y,
                               player_center.y])
        self.thing_group.add(Thing(self.game,
                                   self.x + self.hit_offset.x,
                                   self.y + self.hit_offset.y,
                                   self.thing_key,
                                   player_center))
