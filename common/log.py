import logging

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

# TODO: Probably have an enum of "log levels" and use that instead of the color parameter

def log(message: str, color: str | None = None) -> None:
    if color == Colors.RED:
        print(Colors.RED + "ERROR: " + message + Style.RESET_ALL)
    elif color == Colors.YELLOW:
        print(Colors.YELLOW + "WARNING: " + message + Style.RESET_ALL)
    elif color == Colors.GREEN:
        print(Colors.GREEN + "SUCCESS: " + message + Style.RESET_ALL)
    else:
        print("INFO: " + message)
