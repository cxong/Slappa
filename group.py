class Group(object):
    def __init__(self):
        self.children = []

    def add(self, child):
        self.children.append(child)

    def update(self, time):
        self.children[:] = [child for child in self.children if child.exists()]
        for child in self.children:
            child.update(time)

    def __iter__(self):
        for child in self.children:
            yield child

    def __getitem__(self, item):
        return self.children[item]