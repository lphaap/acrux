from pynput import keyboard
from src.meta.controllable import Controllable
from src.meta.pipeline_input import PipelineInput
from src.pipeline import Pipeline
import src.utils.logger as logger;

class KeyboardListener(PipelineInput, Controllable):

    def __init__(self, pipeline: Pipeline):
        logger.log("KeyboardListener: Init");

        # Init pipeline input parent
        super(KeyboardListener, self).__init__(pipeline)

        self.active = False;
        self.listener =  keyboard.Listener(
            on_press=self.publish,
            on_release=self.publish
        );


    def start(self):
        if self.pipeline == None:
            raise Exception("No pipeline registered")

        self.active = True;
        self.listener.start();

    def stop(self):
        self.active = False;
        self.listener.stop();

    def is_active(self):
        return self.active
