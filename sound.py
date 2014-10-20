'''
Just a dumb reference to a Sound for now
'''
class Sound(object):
    def __init__(self, game, key):
        self.sound = game.load.sounds[key]

    def play(self):
        self.sound.play()