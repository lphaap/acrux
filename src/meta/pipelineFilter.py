import abc

class PipelineFilter(metaclass=abc.ABCMeta):
    def __subclasscheck__(cls, subclass):
        return (
            hasattr(subclass, 'process') and
            callable(subclass.process)
        )


    @abc.abstractmethod
    def process(self, data: any):
        """Process the given data input"""
        raise NotImplementedError
