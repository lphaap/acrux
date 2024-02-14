import traceback
import uuid
from src.utils import logger
from src.pipeline.pipelineData import PipelineData
from src.meta.controllable import Controllable
from src.utils.globals import Globals

class PipelineRunner(Controllable):

    def __init__(self, pipeline, connection):
        self.pipeline = pipeline
        self.connection = connection
        self.running = False
        self.lock = str(uuid.uuid4())
        logger.log('Runner: Init ' + self.lock)

    def isActive(self):
        return self.running

    def start(self):
        logger.log('Runner: Start')
        self.running = True
        try:
            while self.running:
                # Kill execution based on Globals state
                if not Globals.state().isAlive():
                    self.stop()
                    break

                # Wait for data from master thread
                input = self.connection.recv()

                # Disallow new pipeline inserts when locked
                if Globals.lock().isLocked(self.lock):
                    continue

                if 'stop' in input:
                    self.stop()
                    break

                data = PipelineData(self.lock)
                data.set(input)

                for filter in self.pipeline:
                    filter.process(data)
                    if not data.alive():
                        break

                    logger.log(data.get())

        except Exception as e:
            logger.log('Runner: <<< ERROR >>> \n\n' + traceback.format_exc())
            self.stop()

    def stop(self):
        self.running = False
        self.connection.send({ "stop": True })
        logger.log('Runner: Stop')
