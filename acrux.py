from src.utils.fileLoader import FileLoader;
from src.utils.config import Config;
from src.main import init

import src.utils.logger as logger;
import json as json;
import sys

# Skip cli config withouth parameters
if len( sys.argv ) == 1:
    logger.log('Acrux, skipping setup.');

    logger.log("Main: Trying to load default profile.");
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

    init(profileMap);

    exit();

# Load cli bootstrap
import src.bootstrap
