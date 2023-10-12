from src.utils.fileLoader import FileLoader;
import src.utils.logger;
import json;

# A config / settings Borg-class relying on the config.json file
# The borg pattern: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch05s23.html
class Borg:
    sharedState: dict = {};

    def __init__(self) -> None:
        self.__dict__ = self.sharedState


class Config(Borg):

    def __init__(self):
        super().__init__();
        if not hasattr(self, "state"):
            self.state = FileLoader.load("config.json");

    def all(self):
        return self.state;

    def getValue(self, setting: str):
        try:
            return self.state[setting];
        except:
            return None;

    def setValue(self, setting: str, value: str, save = True):
        try:
            self.state[setting] = value;
            if save:
                Config.save();
            return True;
        except:
            return False;

    @staticmethod
    def save():
        config = Config();
        FileLoader.save(
            "config.json",
            json.dumps(config.all(), indent = 4)
        );

    @staticmethod
    def set(setting: str, value: str, save = True):
        return Config().setValue(setting, value, save);

    @staticmethod
    def get(setting: str):
        return Config().getValue(setting);

    @staticmethod
    def reset():
        defaultConfig = json.dumps(
            {
                "latestProfile": None,
                "defaultProfile": None,
                "profileFolder": "profiles/"
            },
            indent = 4
        );

        # Override existing config file
        if FileLoader.exists("config.json"):
            FileLoader.save(
                "config.json",
                defaultConfig
            );
            return;

        # Create one if it does not exist
        FileLoader.create("config.json", defaultConfig);
