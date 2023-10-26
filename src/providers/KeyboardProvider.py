from collections import deque
from types import resolve_bases;
from pynput import keyboard;
import clipboard as clipboard;

class KeyboardProvider():

    def type(self, line: str):
        keyboard.Controller().type(line);

    def press(self, key: any):
        keyboard.Controller().tap(key)

    def pressWithModifier(self, key, modifier):
        keyboard.Controller().press(modifier)
        keyboard.Controller().tap(key)
        keyboard.Controller().release(modifier)
        self.delay(0.01);


    def clearModifiers(self, *args):
        modifiers = [
            keyboard.Key.alt_gr,
            keyboard.Key.alt_l,
            keyboard.Key.alt_r,
            keyboard.Key.alt,
            keyboard.Key.shift,
            keyboard.Key.ctrl,
            keyboard.Key.ctrl_l,
            keyboard.Key.ctrl_r,
        ];

        for key in modifiers:
            keyboard.Controller().release(key);

        self.delay(0.01);
