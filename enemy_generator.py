from enemy import *


class EnemyGenerator(object):
    def __init__(self, enemies, players, things):
        self.spawn_counter = 0
        self.spawn_period = 300
        self.max_enemies = 3
        self.enemies = enemies
        self.players = players
        self.thing_keys = load_things_from_folder("things")
        self.things = things

    def update(self, time):
        self.spawn_counter -= 1
        if self.spawn_counter <= 0:
            self.spawn_counter = self.spawn_period
            if len(self.enemies.children) < self.max_enemies:
                self.enemies.add(Enemy(
                    random.choice([0, SCREEN_SIZE[0]]),
                    FLOOR_Y,
                    'monster',
                    (64, 64),
                    self.players,
                    self.thing_keys,
                    self.things))