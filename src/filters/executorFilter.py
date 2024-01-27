from src.meta.pipelineFilter import PipelineFilter

class ExecutorFilter(PipelineFilter):

    def execute(self, command):
        fn = command[0]
        if (len(command) > 1):
            params = command[1]
            fn(params)
        else:
            fn()

    def process(self, data: any):
        functions = data

        for command in functions:
            if isinstance(command, list):
                for subCommand in functions:
                    self.execute(subCommand)
            else:
                self.execute(command)


        # Filter does not have side-effects
        return functions
