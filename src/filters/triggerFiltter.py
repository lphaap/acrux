from src.pipeline.pipelineData import PipelineData
from src.meta.pipelineFilter import PipelineFilter

class TriggerFilter(PipelineFilter):

    def __init__(self, triggers):
        self.triggers = triggers

    def process(self, data: PipelineData):
        results = []
        if data.get():
            for trigger in self.triggers:
                fn = trigger['function']
                params = trigger['params']

                if (params):
                    result = fn(params)
                else:
                    result = fn()

                if result:
                    results.append(result)

        if len(results) <= 0:
            data.kill()
            return

        data.set(results)
