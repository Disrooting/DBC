"""
=========================================================
 Discord Desktop Client V2
 config.py

 Configuration manager.

 Handles:
    • Loading settings
    • Saving settings
    • Updating values
    • Creating defaults
    • Resetting configuration
=========================================================
"""

import json
import shutil
from pathlib import Path
from copy import deepcopy

from .constants import (
    CONFIG_FILE,
    DEFAULT_CONFIG,
)

from .logger import logger



class ConfigManager:


    def __init__(self):

        self.path = Path(CONFIG_FILE)

        self.data = {}

        self.load()



    # -----------------------------------------------------
    # Load config
    # -----------------------------------------------------

    def load(self):

        try:

            if not self.path.exists():

                logger.info(
                    "Config file not found. Creating default config."
                )

                self.data = deepcopy(DEFAULT_CONFIG)

                self.save()

                return


            with open(
                self.path,
                "r",
                encoding="utf-8"
            ) as file:

                self.data = json.load(file)



            # Add missing values from defaults

            changed = False

            for key, value in DEFAULT_CONFIG.items():

                if key not in self.data:

                    self.data[key] = value

                    changed = True



            if changed:

                self.save()



            logger.info(
                "Configuration loaded successfully."
            )


        except Exception:

            logger.exception(
                "Failed loading configuration. Resetting."
            )

            self.data = deepcopy(DEFAULT_CONFIG)

            self.save()



    # -----------------------------------------------------
    # Save config
    # -----------------------------------------------------

    def save(self):

        try:

            temp_file = self.path.with_suffix(
                ".tmp"
            )


            with open(
                temp_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(

                    self.data,

                    file,

                    indent=4

                )


            # Atomic replace

            shutil.move(

                temp_file,

                self.path

            )


            logger.debug(
                "Configuration saved."
            )


        except Exception:

            logger.exception(
                "Failed saving configuration."
            )



    # -----------------------------------------------------
    # Get value
    # -----------------------------------------------------

    def get(
        self,
        key,
        default=None
    ):

        return self.data.get(
            key,
            default
        )



    # -----------------------------------------------------
    # Set value
    # -----------------------------------------------------

    def set(
        self,
        key,
        value
    ):

        self.data[key] = value

        self.save()



    # -----------------------------------------------------
    # Update multiple values
    # -----------------------------------------------------

    def update(
        self,
        values: dict
    ):

        self.data.update(values)

        self.save()



    # -----------------------------------------------------
    # Remove setting
    # -----------------------------------------------------

    def remove(
        self,
        key
    ):

        if key in self.data:

            del self.data[key]

            self.save()



    # -----------------------------------------------------
    # Reset everything
    # -----------------------------------------------------

    def reset(self):

        logger.warning(
            "Resetting configuration."
        )

        self.data = deepcopy(
            DEFAULT_CONFIG
        )

        self.save()



    # -----------------------------------------------------
    # Token helpers
    # -----------------------------------------------------

    def get_token(self):

        return self.get(
            "token",
            ""
        )



    def save_token(
        self,
        token
    ):

        self.set(
            "token",
            token
        )



    # -----------------------------------------------------
    # Theme helpers
    # -----------------------------------------------------

    def get_theme(self):

        return self.get(
            "theme",
            "dark"
        )



    def set_theme(
        self,
        theme
    ):

        self.set(
            "theme",
            theme
        )



    # -----------------------------------------------------
    # Export
    # -----------------------------------------------------

    def all(self):

        return deepcopy(
            self.data
        )