from copy import deepcopy
from pynput.keyboard import Key, Listener
from src.meta.keyAction import KeyAction
from src.meta.pipelineFilter import PipelineFilter
import src.utils.logger as logger;

class KeyFilter(PipelineFilter):

    def __init__(self):
        self.pressedKeys = []

    def process(self, data: any):
        action = data['action']

        # Priotize pre-parsed canonical key when possible
        rawKey = data['canonical']
        if rawKey == None:
            rawKey = data['key']

        try:
            key = rawKey.char # KeyCode object -> AlphaNumeric
        except:
            key = rawKey.name # Key objects -> Modifiers

        if action == KeyAction.PRESS:
            if key in self.pressedKeys:
                return

            payload = {
                'key': key,
                'modifiers': deepcopy(self.pressedKeys)
            }

            # Handle alt_gr edge case
            if 'alt_gr' in self.pressedKeys:
                for name in ['ctrl', 'ctrl_l']:
                    if name in self.pressedKeys:
                        payload['modifiers'].remove(name)

            self.pressedKeys.append(key)

            return payload

        elif action == KeyAction.RELEASE:
            if key in self.pressedKeys:
                self.pressedKeys.remove(key)

            return None
