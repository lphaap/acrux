import abc

class Controllable(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasscheck__(cls, subclass):
        return (
            hasattr(subclass, 'start') and
            callable(subclass.start) and

            hasattr(subclass, 'stop') and
            callable(subclass.stop) and

            hasattr(subclass, 'isActive') and
            callable(subclass.isActive) and

            hasattr(subclass, 'active')
        )

    @abc.abstractmethod
    def start(self):
        """Start object process"""
        raise NotImplementedError

    @abc.abstractmethod
    def stop(self):
        """Stop object process"""
        raise NotImplementedError

    @abc.abstractmethod
    def isActive(self):
        """Is object process active?"""
        raise NotImplementedError
