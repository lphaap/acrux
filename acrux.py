from src.utils.file_loader import FileLoader;
from src.utils.config import Config;
from src.main import init

import src.utils.logger as logger;
import json as json;
import sys

# Skip cli config withouth parameters
if len( sys.argv ) == 1:
    logger.log('Acrux, skipping setup.');

    logger.log("Main: Trying to load default profile.");
    profile = Config.get("default_profile");

    if not profile:
        logger.log("Main: Trying to load latest profile.");
        profile = Config.get("latest_profile");


    if not profile:
        logger.log("Main: Could not determine profile");
        exit();

    profile_map = FileLoader.load(
        Config.get("profile_folder") + profile
    );
    if not profile_map:
        logger.log("Main: No profile found for latest profile name: '" + profile + "'");
        exit();

    Config.set("latest_profile", profile);
    logger.log("Main: Updated latest profile to: '" + profile + "'");

    init(profile_map);

    exit();

# Load cli bootstrap
import src.bootstrap
