from src.utils.fileLoader import FileLoader;
from src.utils.config import Config;
from src.main import init

import typer;
import inquirer;

import src.utils.logger as logger;
import json as json;
import sys;

def setupDefaultProfile(profile):
    defaultProfile = Config.get("defaultProfile")
    if (defaultProfile == profile):
        return

    query = [
        inquirer.Confirm(
            "confirm",
            message="Do you want to set '" + profile + "' as your default profile?",
            default=True
        ),
    ];

    setDefault = inquirer.prompt(query)["confirm"];
    if setDefault:
        Config.set("defaultProfile", profile);
        logger.log("Main: Updated default profile to: '" + profile + "'");

def setupLatestProfile(profile) -> None:
    latestProfile = Config.get("latestProfile")
    if (latestProfile == profile):
        return

    Config.set("latestProfile", profile);
    logger.log("Main: Updated latest profile to: '" + profile + "'");

def validateFolderPath(current):
    if not current:
        raise inquirer.errors.ValidationError("", reason="Profile folder cannot be empty!");

    if not current.endswith("/"):
        raise inquirer.errors.ValidationError("", reason="Invalid path! Path should end in a '/'.");

    if not FileLoader.exists(current):
        raise inquirer.errors.ValidationError("", reason="Invalid path! No such folder.");

    return True;

# Init typer commands and params:# Init typer CLI interface
init = typer.Typer(help = "Acrux, for all your macroing needs!");

# Select spesific profile
@init.command()
def set(
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

    profileMap = FileLoader.load(Config.get("profileFolder") + profile);
    if not profileMap:
        logger.log("Main: No profile found for given profile name: '" + profile + "'");
        exit();

    setupDefaultProfile(profile);
    setupLatestProfile(profile);

    init(profileMap);
    return;

@init.command()
def select():
    """
    Load all profiles for selection from the specified profile folder.
    """

    logger.log("Main: Enabling profile list selection.");

    fileNames = FileLoader.list(Config.get("profileFolder"));
    if not fileNames:
        logger.log("Main: No profiles found in the specified profile folder.");
        exit();

    query = [
        inquirer.List(
            "profile",
            message="Select the profile to load?",
            choices=fileNames,
        ),
    ];

    profile = inquirer.prompt(query)["profile"];

    profileMap = FileLoader.load(Config.get("profileFolder") + profile);
    if not profileMap:
        logger.log("Main: No profile found for given profile name: '" + profile + "'");
        exit();

    setupDefaultProfile(profile);
    setupLatestProfile(profile);

    init(profileMap);
    return;

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
    profileFolder = Config.get("profileFolder");
    query = [
        inquirer.Confirm(
            "default",
            message="Default profile folder set to '" + profileFolder + "', Would you like to set another?",
            default=False
        ),
    ];

    default = inquirer.prompt(query)["default"];
    if default:
        query = [
            inquirer.Text(
                "folder",
                message="Input profile folder path relative to home folder",
                validate=validateFolderPath
            ),
        ];

        profileFolder = inquirer.prompt(query)["folder"];
        Config.set("profileFolder", profileFolder);

        logger.log("Main: Profile folder set to '" + profileFolder + "'");

    logger.log("Main: Config setup done returning.");
    return;

# Init default config if missing
if not FileLoader.exists("config.json"):
    logger.log("Main: Missing default config, starting config generation.");
    setup();


# Handle running via Typer CLI interface
init();
