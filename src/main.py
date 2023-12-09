from src.filters.executorFilter import ExecutorFilter
from src.filters.functionFilter import FunctionFilter
from src.filters.keyFilter import KeyFilter
from src.filters.hotkeyFilter import HotkeyFilter
from src.keyboardListener import KeyboardListener
from src.pipelineManager import PipelineManager
from src.utils.fileLoader import FileLoader;
from src.utils.config import Config;
import src.utils.logger as logger;

def setup():
    import src.bootstrap

def load():
    logger.log("Main: Trying to load profile.");
    profile = Config.get("defaultProfile");

    if not profile:
        logger.log("Main: Trying to load latest profile.");
        profile = Config.get("latestProfile");

    if not profile:
        logger.log("Main: Could not determine profile");
        exit();

    profileMap = FileLoader.load(
        Config.get("profileFolder") + profile
    );
    if not profileMap:
        logger.log("Main: No profile found for latest profile name: '" + profile + "'");
        exit();

    Config.set("latestProfile", profile);
    logger.log("Main: Updated latest profile to: '" + profile + "'");

    logger.log("Main: Profile selected");

    return profileMap

def init(hotkeyMap: dict):
    pipelineManager = PipelineManager(KeyboardListener)

    macroLine = [
        KeyFilter(), # Remove noice and track pressed keys
        HotkeyFilter(hotkeyMap), # Match pressed keys agains hotkey map
        FunctionFilter(), # Parse hotkey map into functions and params
        ExecutorFilter() # Execute the mapped functions
    ]

    pipelineManager.createPipeline(macroLine)

    logger.log("Main: Starting Acrux");
    pipelineManager.start()
    logger.log("Main: Stopping Acrux");
