"""
=========================================================
 Discord Desktop Client V2
 logger.py

 Central logging system.

 Features:
    • Colored console logging
    • Daily log files
    • Automatic log folder creation
    • Exception logging
    • Rotating log files
=========================================================
"""

import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
import sys

from .constants import (
    LOGS_DIR,
    LOG_FILE_NAME,
    LOG_FORMAT,
    DATE_FORMAT,
)

# --------------------------------------------------------
# Console colors
# --------------------------------------------------------

class Colors:

    RESET = "\033[0m"

    GREY = "\033[90m"

    GREEN = "\033[92m"

    YELLOW = "\033[93m"

    RED = "\033[91m"

    BLUE = "\033[94m"

    MAGENTA = "\033[95m"


LEVEL_COLORS = {

    logging.DEBUG: Colors.GREY,

    logging.INFO: Colors.GREEN,

    logging.WARNING: Colors.YELLOW,

    logging.ERROR: Colors.RED,

    logging.CRITICAL: Colors.MAGENTA,

}


# --------------------------------------------------------
# Colored Formatter
# --------------------------------------------------------

class ColoredFormatter(logging.Formatter):

    def format(self, record):

        color = LEVEL_COLORS.get(record.levelno, Colors.RESET)

        message = super().format(record)

        return f"{color}{message}{Colors.RESET}"


# --------------------------------------------------------
# Logger
# --------------------------------------------------------

logger = logging.getLogger("DiscordClient")

logger.setLevel(logging.DEBUG)

logger.propagate = False


# Prevent duplicate handlers

if not logger.handlers:

    # ---------------- Console ----------------

    console = logging.StreamHandler(sys.stdout)

    console.setLevel(logging.INFO)

    console.setFormatter(

        ColoredFormatter(

            LOG_FORMAT,

            DATE_FORMAT

        )

    )

    logger.addHandler(console)

    # ---------------- File ----------------

    logfile = Path(LOGS_DIR) / LOG_FILE_NAME

    file_handler = TimedRotatingFileHandler(

        logfile,

        when="midnight",

        backupCount=14,

        encoding="utf-8"

    )

    file_handler.setLevel(logging.DEBUG)

    file_handler.setFormatter(

        logging.Formatter(

            LOG_FORMAT,

            DATE_FORMAT

        )

    )

    logger.addHandler(file_handler)


# --------------------------------------------------------
# Convenience functions
# --------------------------------------------------------

def debug(message):

    logger.debug(message)


def info(message):

    logger.info(message)


def warning(message):

    logger.warning(message)


def error(message):

    logger.error(message)


def critical(message):

    logger.critical(message)


def exception(message):

    logger.exception(message)