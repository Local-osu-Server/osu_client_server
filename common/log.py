import logging
from enum import Enum

from colorama import Fore as Colors
from colorama import Style
from colorama import init as colorama_init

colorama_init()

logger: logging.Logger = None  # type: ignore


def setup_logging() -> logging.Logger:

    logging.basicConfig(
        filename="log.log",
        format="%(asctime)s %(message)s",
        filemode="w",
    )

    logger = logging.getLogger()

    logger.setLevel(logging.DEBUG)

    logger.info("Logging setup")

    return logger


class LogTypes(Enum):
    INFO = "INFO"
    ERROR = "ERROR"
    WARNING = "WARNING"
    SUCCESS = "SUCCESS"


def log(message: str, type: LogTypes) -> None:
    if type == LogTypes.ERROR:
        print(Colors.RED + "ERROR: " + message + Style.RESET_ALL)
    elif type == LogTypes.WARNING:
        print(Colors.YELLOW + "WARNING: " + message + Style.RESET_ALL)
    elif type == LogTypes.SUCCESS:
        print(Colors.GREEN + "SUCCESS: " + message + Style.RESET_ALL)
    else:
        print("INFO: " + message)
