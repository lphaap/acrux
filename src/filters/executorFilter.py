from copy import deepcopy
from typing import ParamSpec
from pynput.keyboard import Key, Listener
from src.meta.keyAction import KeyAction
from src.meta.pipelineFilter import PipelineFilter
from src.providers.ClipboardProvider import ClipboardProvider
from src.providers.KeyboardProvider import KeyboardProvider

import src.utils.logger as logger;

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
