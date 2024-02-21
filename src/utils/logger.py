from datetime import datetime
from enum import Enum
from src.utils.config import Config

class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WAR = 2
    ERROR = 3
    SILENT = 4

class Logger:
    def __init__(self):
        """
        Initialize the Logger with a specified log level.

        Parameters:
        - log_level: The desired log level (DEBUG, INFO, WAR, ERROR, SILENT).
        """
        self.log_level = LogLevel.SILENT
        self.log_level_map = {
            'debug': LogLevel.DEBUG,
            'info': LogLevel.INFO,
            'war': LogLevel.WAR,
            'error': LogLevel.ERROR,
            'silent': LogLevel.SILENT
        }

        logLevel = Config.get("logLevel")
        if logLevel:
            self.setLevel(logLevel)

    def log(self, level: LogLevel, msg: str) -> None:
        """
        Log a message with the specified log level if it is equal to or below the current log level.

        Parameters:
        - level: The log level of the message.
        - msg: The message to be logged.
        """
        if self.log_level.value <= level.value:
            timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            try:
                print(timestamp, level.name + ":", msg)
            except Exception as e:
                print(timestamp + f"Error in {level.name} log:", str(e))

    def setLevel(self, log_level: str):
        try:
            parsedLevel = self.log_level_map[log_level]
            self.log_level = parsedLevel
        except Exception as e:
            self.log(LogLevel.ERROR, str(e))

    def info(self, msg: str) -> None:
        """
        Log an informational message.

        Parameters:
        - msg: The message to be logged.
        """
        self.log(LogLevel.INFO, msg)

    def warning(self, msg: str) -> None:
        """
        Log a warning message.

        Parameters:
        - msg: The message to be logged.
        """
        self.log(LogLevel.WAR, msg)

    def error(self, msg: str) -> None:
        """
        Log an error message.

        Parameters:
        - msg: The message to be logged.
        """
        self.log(LogLevel.ERROR, msg)

    def debug(self, msg: str) -> None:
        """
        Log a debug message.

        Parameters:
        - msg: The message to be logged.
        """
        self.log(LogLevel.DEBUG, msg)
