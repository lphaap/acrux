from pynput import keyboard
from src.meta.pipelineInput import PipelineInput
from src.pipelineManager import PipelineManager
from src.meta.keyAction import KeyAction
import src.utils.logger as logger;

class KeyboardListener(PipelineInput):

    def __init__(self, pipeline: PipelineManager):
        logger.log("KeyboardListener: init");

        # Init pipeline input parent
        super(KeyboardListener, self).__init__(pipeline)

        self.active = False;
        self.listener = keyboard.Listener(
            on_press=self.handlePress,
            on_release=self.handleRelease
        );

    def handlePress(self, key):
        self.publish({
            'key': key,
            # Parse key regardles of modifiers
            'canonical': self.listener.canonical(key),
            'action': KeyAction.PRESS
        })

    def handleRelease(self, key):
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

        with self.listener as listener:
            self.active = True;
            listener.join()


    def stop(self):
        logger.log("KeyboardListener: stop")
        self.active = False;
        self.listener.stop();

    def isActive(self):
        return self.active
