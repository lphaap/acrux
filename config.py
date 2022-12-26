from file_loader import FileLoader;
import json;
import logger;

# A config / settings Borg-class relying on the config.json file
# The borg pattern: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch05s23.html
class Borg:
    _shared_state: dict = {};

    def __init__(self) -> None:
        self.__dict__ = self._shared_state


class Config(Borg):

    def __init__(self):
        super().__init__();
        if not hasattr(self, "state"):
            logger.log("Loaded from file");
            self.state = FileLoader.load("config.json");

    def all(self):
        return self.state;

    def get(self, setting: str):
        try:
            return self.state[setting];
        except:
            return None;

    def set(self, setting: str, value: str, save = True):
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
        return Config().set(setting, value, save);

    @staticmethod
    def get(self, setting: str):
        return Config().get(setting);

    @staticmethod
    def create():
        default_config = json.dumps(
            {
                "latest_profile": None,
                "default_profile": None,
                "profile_folder": "profiles/"
            },
            indent = 4
        );
        FileLoader.create("config.json", default_config);



