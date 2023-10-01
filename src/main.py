from src.hotkey_handler import HotkeyHandler;
import src.utils.logger as logger;
import json as json;

# Start Macro listener with the parsed map
def main(macro_map: dict):
    logger.log("Main: Profile selected, starting Acrux.");

    handler = HotkeyHandler(macro_map);
    handler.start();
