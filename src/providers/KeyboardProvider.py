from pynput import keyboard;
import clipboard as clipboard;

class KeyboardProvider():

    def type(line: str):
        keyboard.Controller().type(line);

    def press(key: any):
        keyboard.Controller().tap(key)

    def release(key: any):
        keyboard.Controller().release(key)

    def pressWithModifier(key, modifier):
        keyboard.Controller().press(modifier)
        keyboard.Controller().tap(key)
        keyboard.Controller().release(modifier)


    def clearModifiers(*args):
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
