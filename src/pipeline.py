from src.meta.controllable import Controllable
from src.meta.pipeline_input import PipelineInput
from src.meta.pipeline_filter import PipelineFilter
import src.utils.logger as logger;

class Pipeline(Controllable):

    def __init__(
        self,
        input: PipelineInput.__class__,
        filters: PipelineFilter
    ):
        logger.log("Pipeline: init")
        self.input = input(self)

        self.filters = filters

        self.active = False

    def process(self, data):
        logger.log(data.char)
        logger.log(data.KeyCode)
        for filter in self.filters:
            data = filter.process(data)

    def start(self):
        logger.log("Pipeline: start")
        self.active = True;
        self.input.start();

    def stop(self):
        logger.log("Pipeline: stop")
        self.active = False;
        self.input.stop();

    def is_active(self):
        return self.active;
