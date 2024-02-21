# A config / settings Borg-class relying on the config.json file
# The borg pattern: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch05s23.html
from src.utils.logger import Logger
from src.utils.stateTracker import StateTracker
from src.utils.lockTracker import LockTracker

class Borg:
    singleton: dict = {}

    def __init__(self) -> None:
        self.__dict__ = self.singleton

class Globals(Borg):

    def __init__(self):
        super().__init__()
        if not hasattr(self, "utils"):
            self.utils = {
                'state': StateTracker(),
                'lock': LockTracker(),
                'logger': Logger()
            }

    def _get(self, key: str):
        try:
            return self.utils[key]
        except:
            return None

    @staticmethod
    def get(key: str):
        return Globals()._get(key)

    @staticmethod
    def state():
        return Globals()._get('state')

    @staticmethod
    def log():
        return Globals()._get('logger')

    @staticmethod
    def lock():
        return Globals()._get('lock')
