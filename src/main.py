from src.filters.executorFilter import ExecutorFilter
from src.filters.functionFilter import FunctionFilter
from src.filters.keyFilter import KeyFilter
from src.filters.hotkeyFilter import HotkeyFilter
from src.keyboardListener import KeyboardListener
from src.pipeline import Pipeline
from threading import Condition
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
        FunctionFilter(), # Parse hotkey map into functions and params
        ExecutorFilter()
    ])
    pipeline.start()

    condition = Condition()
    with condition:
        condition.wait()

    logger.log("Main: Stopping Acrux");
    pipeline.stop()
    logger.log("Main: Exit");
