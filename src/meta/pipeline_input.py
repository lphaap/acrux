import abc
from src.pipeline import Pipeline

class PipelineInput(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasscheck__(cls, subclass):
        return (
            hasattr(subclass, 'publish') and
            callable(subclass.publish)
        )

    def __init__(self, pipeline: Pipeline):
        self.pipeline = pipeline;

    def publish(self, input):
        self.pipeline.process(input);
