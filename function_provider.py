from pynput import keyboard, mouse;
from collections import deque;
import logger as logger;
import clipboard as clipboard;
import sys;
import time;

class FunctionProvider:

    def __init__(self):
        self.clipboard_buffer = deque(5*[0], 5);
        self.paused = False;

    def execute(self, func_name: str, func_param: any):
        if (
            self.paused
            and func_name != 'unpause'
            and func_name != 'toggle_pause'
            and func_name != 'stop'
        ):
            logger.log("FunctionProvider: PAUSED not processing -> " + func_name + " " + str(func_param));
            return;

        #try:
        func = getattr(self, func_name);
        func(func_param);
        #except Exception:
            #logger.log("FunctionProvider: ERROR while processing -> " + func_name + " " + str(func_param));

    def copy(self, *args):
        # Save existing clipboard value to keep original state
        original = clipboard.paste();

        # Execute a manual copy
        keyboard.Controller().press(keyboard.Key.ctrl_l);
        self.press('c');
        keyboard.Controller().release(keyboard.Key.ctrl_l);
        self.delay(0.02);

        # Save newly copied value to internal buffer
        copied = clipboard.paste();

        # Restore clipboard state
        clipboard.copy(original);

        if not copied or copied.isspace():
            return;

        self.clipboard_buffer.append(copied);

    def paste(self, *args):

        # Fetch copied value from buffer
        copied = self.clipboard_buffer.pop();

        if not copied or copied.isspace():
            return;

        # Save existing clipboard value to keep original state
        original = clipboard.paste();

        clipboard.copy(copied);

        # Paste
        self.paste_existing();

        # Restore clipboard state
        clipboard.copy(original);

    def add_paste(self, structure):
        self.clipboard_buffer.append(structure);

    def paste_existing(self, *args):
        keyboard.Controller().press(keyboard.Key.ctrl_l);
        self.press('v');
        keyboard.Controller().release(keyboard.Key.ctrl_l);
        self.delay(0.02);

    def stop(self, *args):
        exit();

    def unpause(self, *args):
        self.paused = False;

    def pause(self, *args):
        self.paused = True;

    def toggle_pause(self, *args):
        self.paused = not self.paused;

    def type(self, line: str):
        keyboard.Controller().type(line);

    def press(self, key: any):
        keyboard.Controller().press(key);
        keyboard.Controller().release(key);

    def delay(self, seconds: float):
        time.sleep(seconds);

    def release_modifiers(self, *args):
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
