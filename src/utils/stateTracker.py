
class StateTracker():

    def __init__(self):
        self.state = {
            'active': True,
            'alive': True,
        }

    def isAlive(self):
        return self.state['alive']

    def isActive(self):
        return self.state['active']

    def start(self):
        self.state['active'] = True
        return self

    def stop(self):
        self.state['active'] = False
        return self

    def toggle(self):
        self.state['active'] = not self.state['active']
        return self

    def kill(self):
        self.state['alive'] = False
        return self
