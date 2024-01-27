from src.meta.pipelineFilter import PipelineFilter
from src.providers.StateProvider import StateProvider
from src.providers.ClipboardProvider import ClipboardProvider
from src.providers.KeyboardProvider import KeyboardProvider

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

        stateMap = {
            "state.stop": StateProvider.stop,
            "state.start": StateProvider.start,
            "state.toggle": StateProvider.toggle,
            "state.kill": StateProvider.kill
        }

        self.activeMap = {}
        self.activeMap.update(clipboardMap)
        self.activeMap.update(keyboardMap)
        self.activeMap.update(stateMap)

        self.inactiveMap = {}
        self.inactiveMap.update(stateMap)

    def parseFunction(self, sequence):
        # Only allow state handler function during pause
        map = self.activeMap
        if not StateProvider.isActive():
            map = self.inactiveMap

        # Eg. { "function_name": "function_param" }
        if isinstance(sequence, dict):
            name = list(sequence.keys())[0];
            params = list(sequence.values())[0];
        # Eg. { "function_name" }
        else:
            name = sequence
            params = None

        fn = map.get(name)
        if fn == None:
            return None;

        return (fn, params)

    def process(self, data: any):
        functions = []

        macro = data
        for sequence in macro:
            if isinstance(sequence, list):
                for subSequence in sequence:
                    fn = self.parseFunction(subSequence)
                    if fn:
                        functions.append(fn)
            else:
                fn = self.parseFunction(sequence)
                if fn:
                    functions.append(fn)

        if len(functions) == 0:
            return None

        return functions
