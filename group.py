class Group(object):
    def __init__(self):
        self.children = []

    def add(self, child):
        self.children.append(child)
        return child

    def update(self, time):
        self.children[:] = [
            child for child in self.children if child.exists()]
        for child in self.children:
            child.update(time)

    def draw(self, surface):
        for child in self.children:
            child.draw(surface)

    def exists(self):
        return True

    def destroy(self):
        self.children = []

    def __iter__(self):
        for child in self.children:
            yield child

    def __getitem__(self, item):
        return self.children[item]

    def __len__(self):
        return len(self.children)