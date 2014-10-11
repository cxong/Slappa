from enemy import *


class EnemyGenerator(object):
    def __init__(self, enemies, players, things):
        self.spawn_counter = 0
        self.spawn_period = 100
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
                choice = random.choice([
                    'monster', 'monster',
                    'flying'
                ])
                y = FLOOR_Y
                if choice == 'flying':
                    y = random.randint(100, FLOOR_Y - 100)
                self.enemies.add(Enemy(
                    random.choice([0, SCREEN_SIZE[0]]),
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