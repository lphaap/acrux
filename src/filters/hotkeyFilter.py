from src.pipeline.pipelineData import PipelineData
from src.meta.pipelineFilter import PipelineFilter
from src.providers.KeyboardProvider import KeyboardProvider
from copy import deepcopy

class HotkeyFilter(PipelineFilter):

    def __init__(self, map):
        self.map = self.parseKeyMap(map)

    def process(self, data: PipelineData):
        key = data.get('key')
        modifiers = data.get('modifiers')

        parsedModifier = self.parseModifier(modifiers)

        modifierGroup = self.map.get(parsedModifier)
        if modifierGroup:
            # Use a copy so singleton does not get side-effects
            macro = deepcopy(modifierGroup.get(key))
            if macro:
                KeyboardProvider.release(key)
                KeyboardProvider.clearModifiers()

                data.set(macro)
                return

        data.kill()

    def parseKeyMap(self, map):
        if not isinstance(map, list):
            map = [map]

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
