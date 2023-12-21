from src.meta.pipelineFilter import PipelineFilter
from copy import deepcopy
import src.utils.logger as logger;

class HotkeyFilter(PipelineFilter):

    def __init__(self, map):
        self.map = self.parseKeyMap(map)

    def process(self, data: any):
        key = data['key']
        modifier = self.parseModifier(
            data['modifiers']
        )

        modifierGroup = self.map.get(modifier)
        if modifierGroup:
            # Use a copy so singleton does not get side-effects
            macro = deepcopy(modifierGroup.get(key))
            if macro:
                if (
                    'shift' in modifier or
                    'alt' in modifier or
                    'ctrl' in modifier
                ):
                    # Insert automatic modifier clearing
                    macro.insert(0, "keyboard.clearModifiers")

                return macro

        return None

    def parseKeyMap(self, map):
        parsedMap = {}
        for entry in map:
            trigger = entry['trigger']

            modifier = 'none'
            if 'modifiers' in trigger:
                modifier = self.parseModifier(
                    trigger['modifiers']
                )

            if parsedMap.get(modifier) == None:
                parsedMap[modifier] = {}

            key = trigger['key']
            steps = entry['steps']

            parsedMap[modifier][key] = steps

        return parsedMap

    def parseModifier(self, modifiers):
        if len(modifiers) == 0:
            return 'none'

        if isinstance(modifiers, list):
            # Remove modifiers that are 'None'
            modifiers = [m for m in modifiers if m is not None]

            modifiers.sort()
            return "-".join(modifiers)

        return modifiers
