from src.utils.fileLoader import FileLoader;
from src.meta.borg import Borg;


class StateProvider(Borg):

    def __init__(self):
        super().__init__();
        if not hasattr(self, "state"):
            self.state = {
                "active": True,
                "alive": True
            }

    def isAlive(self):
        return self.state.alive

    def isActive(self):
        return self.state.active

    def start(self):
        self.state.active = True

    def stop(self):
        self.state.active = False

    def toggle(self):
        self.state.active = not self.state.active

    def kill(self):
        self.state.alive = False


    @staticmethod
    def isAlive():
        return StateProvider().isAlive()

    @staticmethod
    def isActive():
        return StateProvider().isActive()

    @staticmethod
    def start():
        StateProvider().start()

    @staticmethod
    def stop():
        StateProvider().stop()

    @staticmethod
    def toggle():
        StateProvider().toggle()

    @staticmethod
    def kill():
        StateProvider().kill()
