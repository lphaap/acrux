from src.filters.functionFilter import FunctionFilter
from src.filters.keyFilter import KeyFilter
from src.filters.hotkeyFilter import HotkeyFilter
from src.keyboardListener import KeyboardListener
from src.pipeline import Pipeline
import src.utils.logger as logger;
import json as json;
import time

# Start Macro listener with the parsed map
def init(hotkeyMap: dict):
    logger.log("Main: Profile selected");
    logger.log("Main: Starting Acrux");

    pipeline = Pipeline(KeyboardListener, [
        KeyFilter(), # Remove noice and track pressed keys
        HotkeyFilter(hotkeyMap), # Match pressed keys agains hotkey map
        FunctionFilter() # Parse hotkey map into functions and params
    ])
    pipeline.start()

    for i in range(0, 10):
        time.sleep(1)

    logger.log("Main: Stopping Acrux");
    pipeline.stop()
    logger.log("Main: Exit");
