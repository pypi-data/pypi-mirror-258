import logging
import os
from pathlib import Path

import tomlkit
from simple_toml_configurator import Configuration

logger = logging.getLogger(__name__)

default_config = {
    "sharepoint": {
        "server": "ewsconsulting.sharepoint.com",
        "site": "https://ewsconsulting.sharepoint.com/sites/teams_mb/",
        "username": "",
        "password": "",
    },
    "github": {
        "username": "",
        "token": "",
    },
    "ewstools": {
        "url": "",
        "host": "",
        "port": "",
        "username": "",
        "password": "",
    },
    "paths": {
        "mount_point": "/mnt/ews_drives",
        "drives": "f;p;r",
        "mappings": "/smuffile001/daten$:f;/smuffile001/qm$:p;/smuffile001/ROHDATEN$:r",
    },
}


class EWSConfiguration(Configuration):
    def __init__(self) -> None:
        config_path = os.environ.get("EWS_CONFIG_PATH", Path.home())
        config_file_name = os.environ.get("EWS_CONFIG_FILENAME", ".ews_config")
        filename = Path(config_path) / f"{config_file_name}.toml"
        existing = {}
        if filename.is_file():
            logger.debug("Reading defaults from existing file")
            existing = tomlkit.loads(filename.read_bytes())
            existing = {**existing, **default_config}
        else:
            logger.debug("Creating new file")  # pragma: no cover

        super().__init__(
            config_path=config_path,
            config_file_name=config_file_name,
            defaults=existing,
            env_prefix="EWS",
        )


EWSSettings = EWSConfiguration()

__all__ = ("EWSSettings",)
