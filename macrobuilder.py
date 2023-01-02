from hotkey_handler import HotkeyHandler;
from file_loader import FileLoader;
from config import Config;

import logger as logger;
import json as json;
import typer;
import inquirer;
import os;

# Init typer CLI interface
init = typer.Typer(help = "MacroBuilder, for all your macroing needs!");

# Init default config if missing
if not FileLoader.exists("config.json"):
    logger.log("Main: Missing default config, generating config.json");
    Config.create();

# Init typer commands and params:

# Start Macro listener with the parsed map
def main(macro_map: dict):
    logger.log("Main: Starting MacroBuilding");

    handler = HotkeyHandler(macro_map);
    handler.start();

# Default to latest
@init.command()
def default():

    """
    Try to load the default profile

    Note: requires one to be set first via the 'select' command
    """

    profile = Config.get("default_profile");

    if not profile:
        logger.log("Main: No default profile available, save one with the 'select' command");
        exit();

    profile_map = FileLoader.load(
        Config.get("profile_folder") + profile
    );
    if not profile_map:
        logger.log("Main: No profile found for latest profile name: '" + profile + "'");
        exit();

    Config.set("latest_profile", profile);
    logger.log("Main: Updated latest profile to: '" + profile + "'");

    main(profile_map);

@init.command()
def latest():

    """
    Try to load the latest profile

    Note: requires one to be set first via the 'select' command
    """

    profile = Config.get("latest_profile");

    if not profile:
        logger.log("Main: No latest profile available generate one first with the 'select' command");
        exit();

    profile_map = FileLoader.load(Config.get("profile_folder") + profile);
    if not profile_map:
        logger.log("Main: No profile found for latest profile name: '" + profile + "'");
        exit();

    set_default = typer.confirm("Do you want to set '" + profile + "' as your default profile?");
    if set_default:
        Config.set("default_profile", profile);
        logger.log("Main: Updated default profile to: '" + profile + "'");

    main(profile_map);
    return;

@init.command()
def select(
    profile: str = typer.Option(
            "",
            help = "The name of the profile to load.",
        )
):
    """
    Try to load a spesific profile defined with the PROFILE param.
    """

    profile_map = FileLoader.load(Config.get("profile_folder") + profile);
    if not profile_map:
        logger.log("Main: No profile found for given profile name: '" + profile + "'");
        exit();

    set_default = typer.confirm("Do you want to set '" + profile + "' as your default profile?");
    if set_default:
        Config.set("default_profile", profile);
        logger.log("Main: Updated default profile to: '" + profile + "'");

    Config.set("latest_profile", profile);
    logger.log("Main: Updated latest profile to: '" + profile + "'");

    main(profile_map);
    return;

# Handle running via Typer CLI interface
init();