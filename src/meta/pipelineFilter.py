import abc

from src.pipeline.pipelineData import PipelineData

class PipelineFilter(metaclass=abc.ABCMeta):
    def __subclasscheck__(cls, subclass):
        return (
            hasattr(subclass, 'process') and
            callable(subclass.process)
        )


    @abc.abstractmethod
    def process(self, data: PipelineData):
        """Process the given data input"""
        raise NotImplementedError
