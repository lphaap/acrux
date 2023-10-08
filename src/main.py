from src.keyboard_listener import KeyboardListener
from src.pipeline import Pipeline
import src.utils.logger as logger;
import json as json;
import time

# Start Macro listener with the parsed map
def init(macro_map: dict):
    logger.log("Main: Profile selected, starting Acrux.");

    pipeline = Pipeline(KeyboardListener, [])
    pipeline.start()

    for i in range(0, 5):
        time.sleep(1)

    pipeline.stop()
