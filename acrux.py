from src.main import init, load, setup
from multiprocessing import Process
from src.utils.globals import Globals
from src.utils.config import Config
import json as json
import sys

# Only run setup when master thread is spawned
if __name__ == '__main__':

    # Initialize global utils
    Globals()

    # Skip cli config withouth parameters
    if len( sys.argv ) == 1:

        Globals.log().info("Main: Loading profiles")
        profile = load()

        Globals.log().info("Main: Spawning process")
        mainProcess = Process(target=init, args=(profile,))
        mainProcess.start()

    else:
        Globals.log().info("Main: Running setup")
        setup()
