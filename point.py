class Point(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def multiply(self, other):
        return Point(self.x * other.x, self.y * other.y)