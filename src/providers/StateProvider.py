from src.utils.globals import Globals

class StateProvider():

    def isAlive():
        return Globals.state().isAlive()

    def isActive():
        return Globals.state().isActive()

    def start():
        Globals.state().start()

    def stop():
        Globals.state().stop()

    def toggle():
        Globals.state().toggle()

    def kill():
        Globals.state().kill()
