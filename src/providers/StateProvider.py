# A config / settings Borg-class relying on the config.json file
# The borg pattern: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch05s23.html
class Borg:
    sharedState: dict = {};

    def __init__(self) -> None:
        self.__dict__ = self.sharedState

class StateProvider(Borg):

    def __init__(self):
        super().__init__();
        if not hasattr(self, "state"):
            self.state = {
                'active': True,
                'alive': True
            }

    def _isAlive(self):
        print(self.state)
        return self.state['alive']

    def _isActive(self):
        return self.state['active']

    def _start(self):
        self.state['active'] = True

    def _stop(self):
        self.state['active'] = False

    def _toggle(self):
        self.state['active'] = not self.state['active']

    def _kill(self):
        self.state['alive'] = False


    @staticmethod
    def isAlive(*args):
        return StateProvider()._isAlive()

    @staticmethod
    def isActive(*args):
        return StateProvider()._isActive()

    @staticmethod
    def start(*args):
        return StateProvider()._start()

    @staticmethod
    def stop(*args):
        return StateProvider()._stop()

    @staticmethod
    def toggle(*args):
        return StateProvider()._toggle()

    @staticmethod
    def kill(*args):
        return StateProvider()._kill()
