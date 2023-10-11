from src.filters.key_filter import KeyFilter
from src.keyboard_listener import KeyboardListener
from src.pipeline import Pipeline
import src.utils.logger as logger;
import json as json;
import time

# Start Macro listener with the parsed map
def init(macro_map: dict):
    logger.log("Main: Profile selected");
    logger.log("Main: Starting Acrux");

    pipeline = Pipeline(KeyboardListener, [KeyFilter()])
    pipeline.start()

    for i in range(0, 10):
        time.sleep(1)

    logger.log("Main: Stopping Acrux");
    pipeline.stop()
    logger.log("Main: Exit");
