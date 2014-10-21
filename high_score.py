import datetime
import errno
import locale
import os
import pickle


class HighScore(object):
    def __init__(self):
        locale.setlocale(locale.LC_TIME, '')
        self.dir = os.path.join(os.path.expanduser('~'), '.slappa')
        self.filename = os.path.join(self.dir, 'scores.dat')
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
        # Create the path if not exists
        try:
            os.makedirs(self.dir)
        except OSError as e:
            if e.errno == errno.EEXIST and os.path.isdir(self.dir):
                pass
            else:
                raise
        with open(self.filename, 'wb') as f:
            pickle.dump(self.scores, f)

    def get_scores(self):
        for scores in sorted(self.scores, key=lambda x: x[0], reverse=True):
            yield scores