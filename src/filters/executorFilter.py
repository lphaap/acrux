from src.meta.pipelineFilter import PipelineFilter

class ExecutorFilter(PipelineFilter):

    def process(self, data: any):
        functions = data
        for definition in functions:
            function = definition[0]
            params = definition[1]

            if not function == None:
                function(params)

        # Filter does not have side-effects
        return functions
