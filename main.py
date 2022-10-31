from hotkey_handler import HotkeyHandler;
import logger as logger;
import json as json;

key_map = open("profile.json").read();
handler = HotkeyHandler(json.loads(key_map));
handler.start();
