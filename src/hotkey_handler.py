from pynput import keyboard;
from src.function_provider import FunctionProvider;
import src.utils.logger as logger;
import sys;
import time;
import json;

class HotkeyHandler():

    def __init__(self, key_map: dict):
        logger.log("HotkeyHandler: Init");
        self.hotkey_map = {};
        self.function_provider = FunctionProvider();
        self.special_key_map = {
            "|esc|": keyboard.Key.esc,
            "|space|": keyboard.Key.space,
            "|tab|": keyboard.Key.tab,
            "|enter|": keyboard.Key.enter,
            "|backspace|": keyboard.Key.backspace,
        };
        self.load(key_map);


    def start(self):
        with keyboard.GlobalHotKeys(self.hotkey_map) as listener:
            logger.log("HotkeyHandler: Listener started");
            listener.join();


    def load(self, key_map: dict):

        for entry in key_map.values():
            try:
                modifiers = entry["modifiers"];
            except KeyError:
                modifiers = None;

            try:
                key = entry["key"];
                steps = entry["steps"];
            except KeyError:
                logger.log("HotkeyHandler: ERROR - Missing key or function in key map");
                exit("EXECUTION STOPPED");

            if not isinstance(modifiers, list):
                modifiers = [modifiers];

            listener_key = key.lower();
            for modifier in modifiers:
                listener_key = "<" + modifier.lower() + ">" + "+" + listener_key;

            logger.log("HotkeyHandler: Mapping " + listener_key + " to " + json.dumps(steps));

            self.hotkey_map[listener_key] = self.callback(steps);


    def callback(self, macro_steps: list):
        return lambda : self.handle(macro_steps);


    def handle(self, macro_steps: list):
        if not isinstance(macro_steps, list):
            macro_steps = [macro_steps];

        for step in macro_steps:

            # Eg. { "function_name": "function_param" }
            if isinstance(step, dict):
                func = list(step.keys())[0];
                param = list(step.values())[0];

                # Handle special key values
                if param in self.special_key_map:
                    param = self.special_key_map[param];

            # Eg. { "function_name" }
            else:
                func = step;
                param = None;

            logger.log("HotkeyHandler: Executing -> " + func + " " + str(param));

            self.function_provider.execute(func, param);
