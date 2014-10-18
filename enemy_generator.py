from enemy import *


class EnemyGenerator(object):
    def __init__(self, game, enemies, players, things):
        self.game = game
        self.spawn_counter = 0
        self.spawn_period = 100
        self.max_enemies = 3
        self.enemies = enemies
        self.players = players
        self.thing_keys = load_things_from_folder("things")
        self.things = things

    def update(self, time):
        self.spawn_counter -= ANIM_FRAME_RATE / FRAME_RATE
        if self.spawn_counter <= 0:
            self.spawn_counter = self.spawn_period
            if len(self.enemies.children) < self.max_enemies:
                choice = random.choice([
                    'zombie',
                    'monster',
                    'flying'
                ])
                y = FLOOR_Y

                if choice == 'flying':
                    pad = self.game.height * 0.16
                    y = random.randint(int(pad), int(FLOOR_Y - pad))
                self.enemies.add(Enemy(
                    self.game,
                    random.choice([0, self.game.width]),
                    y,
                    choice,
                    self.players,
                    self.thing_keys,
                    self.things))
                # Step it up: increase rate of spawning
                self.spawn_period -= 10
                if self.spawn_period <= 0:
                    # Really step it up
                    self.max_enemies += 1
                    self.spawn_period = 100