from src.utils.globals import Globals

class LockProvider():

    def lock(key):
        Globals.lock().lock(key)

    def unlock(key):
        Globals.lock().unlock(key)

    def isLocked(key):
        return Globals.lock().isLocked(key)
