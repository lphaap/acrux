# A config / settings Borg-class relying on the config.json file
# The borg pattern: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch05s23.html
class Borg:
    sharedState: dict = {};

    def __init__(self) -> None:
        self.__dict__ = self.sharedState
