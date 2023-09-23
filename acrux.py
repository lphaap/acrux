from hotkey_handler import HotkeyHandler;
from file_loader import FileLoader;
from config import Config;

import logger as logger;
import json as json;
import typer;
import inquirer;
import os;

# Init typer commands and params:# Init typer CLI interface
init = typer.Typer(help = "MacroBuilder, for all your macroing needs!");

# Start Macro listener with the parsed map
def main(macro_map: dict):
    logger.log("Main: Profile selected, starting MacroBuilding.");

    handler = HotkeyHandler(macro_map);
    handler.start();

# Default to latest
@init.command()
def default():

    """
    Try to load the default profile

    Note: requires one to be set first via the 'select' command
    """

    logger.log("Main: Loading default profile.");

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

    logger.log("Main: Loading latest profile.");

    profile = Config.get("latest_profile");

    if not profile:
        logger.log("Main: No latest profile available generate one first with the 'select' command");
        exit();

    profile_map = FileLoader.load(Config.get("profile_folder") + profile);
    if not profile_map:
        logger.log("Main: No profile found for latest profile name: '" + profile + "'");
        exit();

    query = [
        inquirer.Confirm(
            "confirm",
            message="Do you want to set '" + profile + "' as your default profile?",
            default=True
        ),
    ];

    set_default = inquirer.prompt(query)["confirm"];
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

    logger.log("Main: Selecting profile '" + profile + "'");

    if not profile:
        logger.log("Main: No profile given aborting");
        exit();

    profile_map = FileLoader.load(Config.get("profile_folder") + profile);
    if not profile_map:
        logger.log("Main: No profile found for given profile name: '" + profile + "'");
        exit();

    query = [
        inquirer.Confirm(
            "confirm",
            message="Do you want to set '" + profile + "' as your default profile?",
            default=True
        ),
    ];

    set_default = inquirer.prompt(query)["confirm"];
    if set_default:
        Config.set("default_profile", profile);
        logger.log("Main: Updated default profile to: '" + profile + "'");

    Config.set("latest_profile", profile);
    logger.log("Main: Updated latest profile to: '" + profile + "'");

    main(profile_map);
    return;

@init.command()
def list():
    """
    Load all profiles for selection from the specified profile folder.
    """

    logger.log("Main: Enabling profile list selection.");

    file_names = FileLoader.list(Config.get("profile_folder"));
    if not file_names:
        logger.log("Main: No profiles found in the specified profile folder.");
        exit();

    query = [
        inquirer.List(
            "profile",
            message="Select the profile to load?",
            choices=file_names,
        ),
    ];

    selected_profile = inquirer.prompt(query)["profile"];

    profile_map = FileLoader.load(Config.get("profile_folder") + selected_profile);
    if not profile_map:
        logger.log("Main: No profile found for given profile name: '" + selected_profile + "'");
        exit();

    main(profile_map);
    return;

# Handler for profile folder path validation
def _validate_folder_path(answers, current):
    if not current:
        raise inquirer.errors.ValidationError("", reason="Profile folder cannot be empty!");

    if not current.endswith("/"):
        raise inquirer.errors.ValidationError("", reason="Invalid path! Path should end in a '/'.");

    if not FileLoader.exists(current):
        raise inquirer.errors.ValidationError("", reason="Invalid path! No such folder.");

    return True;

@init.command()
def setup():
    """
    Run an intial setup and configurations.
    """

    logger.log("Main: Starting config setup.");

    # Handle existing config file
    if FileLoader.exists("config.json"):
        query = [
            inquirer.Confirm(
                "reset",
                message="A config file already exists. Would you like to reset it?",
                default=False
            ),
        ];

        reset = inquirer.prompt(query)["reset"];
        if not reset:
            logger.log("Main: Aborting config setup.");
            exit();

    Config.reset();

    # Query default config usage
    query = [
        inquirer.Confirm(
            "default",
            message="Would you like to use the default config?",
            default=False

        ),
    ];

    default = inquirer.prompt(query)["default"];
    if default:
        logger.log("Main: Config setup done returning.");
        return;


    # Query default config usage
    profile_folder = Config.get("profile_folder");
    query = [
        inquirer.Confirm(
            "default",
            message="Default profile folder set to '" + profile_folder + "', Would you like to set another?",
            default=False
        ),
    ];

    default = inquirer.prompt(query)["default"];
    if default:
        query = [
            inquirer.Text(
                "folder",
                message="Input profile folder path relative to home folder",
                validate=_validate_folder_path
            ),
        ];

        profile_folder = inquirer.prompt(query)["folder"];
        Config.set("profile_folder", profile_folder);

        logger.log("Main: Profile folder set to '" + profile_folder + "'");

    logger.log("Main: Config setup done returning.");
    return;

# Init default config if missing
if not FileLoader.exists("config.json"):
    logger.log("Main: Missing default config, starting config generation.");
    setup();


# Handle running via Typer CLI interface
init();