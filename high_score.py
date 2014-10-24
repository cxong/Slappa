import datetime
import errno
import locale
import os
import pickle
import sys


"""
Douglas Mayle
http://stackoverflow.com/users/8458/douglas-mayle
http://stackoverflow.com/a/1088459/2038264
http://creativecommons.org/licenses/by-sa/3.0/
"""


def get_app_data(app_name):
    if sys.platform == 'darwin':
        from AppKit import NSSearchPathForDirectoriesInDomains
        # http://developer.apple.com/DOCUMENTATION/Cocoa/Reference/Foundation/Miscellaneous/Foundation_Functions/Reference/reference.html#//apple_ref/c/func/NSSearchPathForDirectoriesInDomains
        # NSApplicationSupportDirectory = 14
        # NSUserDomainMask = 1
        # True for expanding the tilde into a fully qualified path
        app_data = os.path.join(
            NSSearchPathForDirectoriesInDomains(14, 1, True)[0], app_name)
    elif sys.platform == 'win32':
        app_data = os.path.join(os.environ['APPDATA'], app_name)
    else:
        app_data = os.path.expanduser(os.path.join("~", "." + app_name))
    return app_data


class HighScore(object):
    def __init__(self):
        locale.setlocale(locale.LC_TIME, '')
        self.dir = get_app_data('slappa')
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