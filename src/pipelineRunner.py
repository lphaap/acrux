
from src.utils import logger
from src.meta.controllable import Controllable
from src.providers.StateProvider import StateProvider

class PipelineRunner(Controllable):

    def __init__(self, pipeline, connection):
        logger.log('Runner: Init')
        self.pipeline = pipeline
        self.connection = connection
        self.running = False

    def isActive(self):
        return self.running

    def start(self):
        logger.log('Runner: Start')
        self.running = True
        try:
            while self.running:
                if not StateProvider.isAlive():
                    self.stop()
                    break

                # Wait for data
                data = self.connection.recv()

                try:
                    # Stop called by manager thread
                    if data['stop']:
                        self.stop()
                        break
                except:
                    for filter in self.pipeline:
                        data = filter.process(data)
                        if data == None:
                            break

                        logger.log(data)
        except:
            logger.log('Runner: ERROR')
            self.stop()

    def stop(self):
        self.running = False
        self.connection.send({ "stop": True })
        logger.log('Runner: Stop')
