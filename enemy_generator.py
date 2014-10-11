class EnemyGenerator(object):
    def __init__(self):
        self.spawn_counter = 300

    def update(self, time):
        self.spawn_counter -= 1
        if self.spawn_counter <= 0:
            self.spawn_counter = 300
