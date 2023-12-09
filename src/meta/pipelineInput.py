import abc
from src.meta.controllable import Controllable

# Avoid circular dependecies during type checking
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.pipelineManager import Pipeline

class PipelineInput(Controllable, metaclass=abc.ABCMeta):
    @classmethod
    def __subclasscheck__(cls, subclass):
        return (
            hasattr(subclass, 'publish') and
            callable(subclass.publish)
        )

    def __init__(self, pipeline: 'Pipeline'):
        self.pipeline = pipeline;

    def publish(self, input):
        self.pipeline.process(input);
