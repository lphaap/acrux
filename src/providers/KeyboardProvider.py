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
