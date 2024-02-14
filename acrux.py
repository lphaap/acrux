from src.main import init, load, setup;
from multiprocessing import Process;
import src.utils.logger as logger;
from src.utils.globals import Globals;
import json as json;
import sys

# Only run setup when master thread is spawned
if __name__ == '__main__':

    # Initialize global utils
    Globals()

    # Skip cli config withouth parameters
    if len( sys.argv ) == 1:

        logger.log("Main: Loading profiles");
        profile = load()

        logger.log("Main: Spawning process");
        mainProcess = Process(target=init, args=(profile,))
        mainProcess.start()

    else:
        logger.log("Main: Running setup");
        setup()
