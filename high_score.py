import datetime
import locale
import pickle
from os.path import expanduser, join


class HighScore(object):
    def __init__(self):
        locale.setlocale(locale.LC_TIME, '')
        self.filename = join(expanduser('~'), '.slappa', 'scores.dat')
        # Load existing high scores
        try:
            with open(self.filename, 'rb') as f:
                self.scores = pickle.load(f)
        except:
            self.scores = []

    def get_date(self):
        return datetime.date.today().strftime('%x')

    def add(self, score, name):
        date = self.get_date()
        self.scores.append([score, name, date])
        with open(self.filename, 'wb') as f:
            pickle.dump(self.scores, f)

    def get_scores(self):
        for scores in sorted(self.scores, key=lambda x: x[0], reverse=True):
            yield scores