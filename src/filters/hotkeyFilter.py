from copy import deepcopy
from pynput.keyboard import Key, Listener
from src.meta.keyAction import KeyAction
from src.meta.pipelineFilter import PipelineFilter

import src.utils.logger as logger;

class HotkeyFilter(PipelineFilter):

    def __init__(self, map):
        self.map = self.parseKeyMap(map)

    def process(self, data: any):
        key = data['key']
        modifier =  self.parseModifier(
            data['modifiers']
        )

        modifierGroup = self.map.get(modifier)
        if modifierGroup:
            macro = modifierGroup.get(key)
            if macro:
                return macro

        return None

    def parseKeyMap(self, map):
        parsedMap = {}
        for entry in map.values():
            modifier = 'none'
            if 'modifiers' in entry:
                modifier = self.parseModifier(
                    entry['modifiers']
                )
            key = entry['key']
            macro = entry['steps']

            if parsedMap.get(modifier) == None:
                parsedMap[modifier] = {}

            parsedMap[modifier][key] = macro

        logger.log(parsedMap)

        return parsedMap

    def parseModifier(self, modifiers):
        if len(modifiers) == 0:
            return 'none'

        if isinstance(modifiers, list):
            modifiers.sort()
            return "-".join(modifiers)

        return modifiers
