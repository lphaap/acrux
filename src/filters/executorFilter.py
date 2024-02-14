from src.pipeline.pipelineData import PipelineData
from src.meta.pipelineFilter import PipelineFilter
from src.utils.globals import Globals

class ExecutorFilter(PipelineFilter):

    def execute(self, command):
        fn = command[0]
        if (len(command) > 1 and command[1]):
            params = command[1]
            fn(params)
        else:
            fn()

    # Filter does not have side-effects
    def process(self, data: PipelineData):
        functions = data.get()

        for command in functions:
            if isinstance(command, list):
                for subCommand in command:
                    self.execute(subCommand)
            else:
                self.execute(command)

        data.kill()
