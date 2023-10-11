from pynput import keyboard
from src.meta.pipeline_input import PipelineInput
from src.pipeline import Pipeline
from src.meta.key_action import KeyAction
import src.utils.logger as logger;

class KeyboardListener(PipelineInput):

    def __init__(self, pipeline: Pipeline):
        logger.log("KeyboardListener: init");

        # Init pipeline input parent
        super(KeyboardListener, self).__init__(pipeline)

        self.active = False;
        self.listener = keyboard.Listener(
            on_press=self.handle_press,
            on_release=self.handle_release
        );

    def handle_press(self, key):
        self.publish({
            'key': key,
            # Parse key regardles of modifiers
            'canonical': self.listener.canonical(key),
            'action': KeyAction.PRESS
        })

    def handle_release(self, key):
        self.publish({
            'key': key,
            # Parse key regardles of modifiers
            'canonical': self.listener.canonical(key),
            'action': KeyAction.RELEASE
        })

    def start(self):
        logger.log("KeyboardListener: start")
        if self.pipeline == None:
            raise Exception("No pipeline registered")

        self.active = True;
        self.listener.start();

    def stop(self):
        logger.log("KeyboardListener: stop")
        self.active = False;
        self.listener.stop();

    def is_active(self):
        return self.active
