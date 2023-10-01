from pynput import keyboard
from src.meta.pipeline_input import PipelineInput
from src.utils.logger import logger

class KeyboardListener(PipelineInput):

    def __init__(self, pipeline):
        logger.log("KeyboardListener: Init");
        self.pipeline = pipeline;
        self.active = False;
        self.listener =  keyboard.Listener(
            on_press=self.publish_input,
            on_release=self.publish_input
        );

    def publish_input(self, input):
        self.pipeline.input(input)

    def start(self):
        self.active = True
        self.listener.start()

    def stop(self):
        self.active = False
        self.listener.stop()
