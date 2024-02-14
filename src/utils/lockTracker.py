
class LockTracker():

    def __init__(self):
        self.locks = list()

    def lock(self, key):
        if not self.isLocked(key):
            self.locks.append(key)

        return self

    def unlock(self, key):
        if self.isLocked(key):
            self.locks.remove(key)

        return self

    def isLocked(self, key):
        return key in self.locks
