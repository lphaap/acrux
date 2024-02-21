from src.filters.triggerFiltter import TriggerFilter
from src.filters.executorFilter import ExecutorFilter
from src.filters.functionFilter import FunctionFilter
from src.filters.keyFilter import KeyFilter
from src.filters.hotkeyFilter import HotkeyFilter
from src.providers.GuiProvider import GuiProvider
from src.pipeline.keyboardListener import KeyboardListener
from src.pipeline.pipelineManager import PipelineManager
from src.utils.fileLoader import FileLoader
from src.utils.config import Config
from src.utils.globals import Globals

def setup():
    import src.bootstrap

def load():
    Globals.log().info("Main: Trying to load profile.")
    profile = Config.get("defaultProfile")

    if not profile:
        Globals.log().info("Main: Trying to load latest profile.")
        profile = Config.get("latestProfile")

    if not profile:
        Globals.log().info("Main: Could not determine profile")
        exit()

    profileMap = FileLoader.load(
        Config.get("profileFolder") + profile
    )
    if not profileMap:
        Globals.log().info("Main: No profile found for latest profile name: '" + profile + "'")
        exit()

    Config.set("latestProfile", profile)
    Globals.log().info("Main: Updated latest profile to: '" + profile + "'")

    Globals.log().info("Main: Profile selected")

    return profileMap

def init(profile: dict):
    pipelineManager = PipelineManager(KeyboardListener)

    if "macros" in profile:
        macroPipeline = [
            KeyFilter(), # Remove noice and track pressed keys
            HotkeyFilter(profile['macros']), # Match pressed keys against hotkey map
            FunctionFilter(), # Parse hotkey map into functions and params
            ExecutorFilter() # Execute the mapped functions
        ]

        Globals.log().info("Main: Setting up macro pipeline")
        pipelineManager.createPipeline(macroPipeline)

    if "functions" in profile:
        startupHotkey = profile['functions']['startup']

        actionMap = {}
        for action in profile['functions']['actions']:
            actionMap[action['identifier']] = action['steps']

        functionPipeline = [
            KeyFilter(), # Remove noice and track pressed keys
            HotkeyFilter(startupHotkey), # Pass selected startup hotkey
            TriggerFilter([{ # Trigger searh GUI after hotkey pass
                "function": GuiProvider.search,
                "params": actionMap
            }]),
            FunctionFilter(), # Parse selected function into executable one
            ExecutorFilter() # Execute the selected function from search
        ]

        Globals.log().info("Main: Setting up function pipeline")
        pipelineManager.createPipeline(functionPipeline)

    Globals.log().info("Main: Starting Acrux")
    pipelineManager.start()
    Globals.log().info("Main: Stopping Acrux")
