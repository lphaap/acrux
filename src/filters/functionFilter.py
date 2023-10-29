from copy import deepcopy
from pynput.keyboard import Key, Listener
from src.meta.keyAction import KeyAction
from src.meta.pipelineFilter import PipelineFilter
from src.providers.ClipboardProvider import ClipboardProvider
from src.providers.KeyboardProvider import KeyboardProvider

import src.utils.logger as logger;

class FunctionFilter(PipelineFilter):

    def __init__(self):
        clipboard = ClipboardProvider()
        clipboardMap = {
            "clipboard.copy": clipboard.copy,
            "clipboard.paste": clipboard.paste,
            "clipboard.save": clipboard.save,
            "clipboard.pressCopy": clipboard.pressCopy,
            "clipboard.pressPaste": clipboard.pressPaste
        }

        keyboard = KeyboardProvider()
        keyboardMap = {
            "keyboard.press": keyboard.press,
            "keboard.pressWithModifiers": keyboard.pressWithModifier,
            "keyboard.type": keyboard.type,
            "keyboard.clearModifiers": keyboard.clearModifiers
        }

        self.map = {}
        self.map.update(clipboardMap)
        self.map.update(keyboardMap)

    def process(self, data: any):
        functions = []

        macro = data
        for fn in macro:
            # Eg. { "function_name": "function_param" }
            if isinstance(fn, dict):
                name = list(fn.keys())[0];
                params = list(fn.values())[0];
            # Eg. { "function_name" }
            else:
                name = fn
                params = None

            function = self.map.get(name)
            if function == None:
                continue;

            functions.append((function, params))

        if len(functions) == 0:
            return None

        return functions
