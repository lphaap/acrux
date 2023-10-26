from collections import deque;

import clipboard as clipboard;
from src.providers.KeyboardProvider import KeyboardProvider

import src.utils.logger as logger;

class ClipboardProvider():
    def __init__(self):
        self.buffer = deque(5*[0], 5);

    def copy(self, *args):
        # Save existing clipboard value to keep original state
        original = clipboard.paste();

        self.pressCopy()

        # Save newly copied value to internal buffer
        copied = clipboard.paste();

        # Restore clipboard state
        clipboard.copy(original);

        if (
            not copied
            or copied.isspace()
            or copied == original
        ):
            return;

        self.buffer.append(copied);

    def paste(self, *args):

        # Fetch copied value from buffer
        copied = None;
        try:
            copied = self.buffer.pop();
        except IndexError:
            logger.log("FunctionProvider: Notice -> Nothing to paste");
            return;

        if not copied or copied.isspace():
            return;

        # Save existing clipboard value to keep original state
        original = clipboard.paste();

        clipboard.copy(copied);

        # Paste
        self.pressPaste();

        # Restore clipboard state
        clipboard.copy(original);

    def saveToClipboard(self, structure):
        self.buffer.append(structure);

    def pressCopy(self, *args):
        KeyboardProvider.pressWithModifier('c', 'ctrl_l')
        self.delay(0.02);

    def pressPaste(self, *args):
        KeyboardProvider.pressWithModifier('v', 'ctrl_l')
        self.delay(0.02);
