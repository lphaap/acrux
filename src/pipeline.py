from src.meta.controllable import Controllable
from src.meta.pipelineInput import PipelineInput
from src.meta.pipelineFilter import PipelineFilter
from pynput.keyboard import Key
import src.utils.logger as logger;

class Pipeline(Controllable):

    def __init__(
        self,
        input: PipelineInput.__class__,
        filters: PipelineFilter
    ):
        logger.log("Pipeline: build")
        self.input = input(self)

        self.filters = filters

        self.active = False

    def process(self, data):
        # logger.log(data)
        for filter in self.filters:
            data = filter.process(data)
            if data == None:
                return

            logger.log(data)

    def start(self):
        logger.log("Pipeline: start")
        self.active = True;
        self.input.start();

    def stop(self):
        logger.log("Pipeline: stop")
        self.active = False;
        self.input.stop();

    def isActive(self):
        return self.active;
