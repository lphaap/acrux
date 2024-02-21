from src.pipeline.pipelineData import PipelineData
from src.meta.pipelineFilter import PipelineFilter
from src.utils.globals import Globals
from src.providers.ClipboardProvider import ClipboardProvider
from src.providers.KeyboardProvider import KeyboardProvider
from src.providers.ExeProvider import ExeProvider
from src.providers.TimeProvider import TimeProvider
from src.providers.StateProvider import StateProvider
from src.providers.LockProvider import LockProvider

def gg():
    Globals.state().kill()

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

        keyboardMap = {
            "keyboard.press": KeyboardProvider.press,
            "keboard.pressWithModifiers": KeyboardProvider.pressWithModifier,
            "keyboard.type": KeyboardProvider.type,
            "keyboard.clearModifiers": KeyboardProvider.clearModifiers
        }

        timeMap = {
            "time.sleep": TimeProvider.sleep
        }

        stateMap = {
            "state.stop": StateProvider.stop,
            "state.start": StateProvider.start,
            "state.toggle": StateProvider.toggle,
            "state.kill": StateProvider.kill
        }

        exeMap = {
            "exe.execute": ExeProvider.execute
        }

        self.lockRequired = [
            "keyboard.press",
            "keboard.pressWithModifiers",
            "keyboard.type"
        ]

        self.activeMap = {}
        self.activeMap.update(clipboardMap)
        self.activeMap.update(keyboardMap)
        self.activeMap.update(timeMap)
        self.activeMap.update(stateMap)
        self.activeMap.update(exeMap)

        self.inactiveMap = {}
        self.inactiveMap.update(stateMap)

    def parseFunction(self, sequence):
        # Only allow state handler function during pause
        map = self.activeMap
        if not Globals.state().isActive():
            map = self.inactiveMap

        # Eg. { "function_name": "function_param" }
        if isinstance(sequence, dict):
            name = list(sequence.keys())[0]
            params = list(sequence.values())[0]
        # Eg. { "function_name" }
        else:
            name = sequence
            params = None

        fn = map.get(name)
        if fn == None:
            return None

        return (fn, params)

    def requiresLock(self, sequence):
        if isinstance(sequence, dict):
            name = list(sequence.keys())[0]
        else:
            name = sequence

        return name in self.lockRequired


    def process(self, data: PipelineData):
        macros = data.get()

        functions = []
        for macroSequence in macros:
            sequences = macroSequence
            if not isinstance(macroSequence, list):
                sequences = [macroSequence]

            for sequence in sequences:
                fn = self.parseFunction(sequence)
                if fn:
                    if self.requiresLock(sequence):
                        functions.append((LockProvider.lock, data.id()))
                        functions.append(fn)
                        functions.append((LockProvider.unlock, data.id()))
                    else:
                        functions.append(fn)

        if len(functions) == 0:
            data.kill()
            return

        data.set(functions)
