class Array:
    def __init__(self, a=[]):
        self.a = a
        self.c = 0

    def append(self, q):
        self.a += [q]
        self.c += 1
        return self.a

    def delete(self, index=None, value=None):
        for i in range(self.c):
            if index == i or value == self.a[i]:
                del self.a[i]
                return self.a