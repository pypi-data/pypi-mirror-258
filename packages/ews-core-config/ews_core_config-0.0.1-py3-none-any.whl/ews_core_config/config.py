import logging
import os
from pathlib import Path

from simple_toml_configurator import Configuration

logger = logging.getLogger(__name__)

default_config = {
    "sharepoint": {
        "server": "",
        "site": "",
        "username": "",
        "password": "",
    },
    "github": {
        "token": "",
    },
    "paths": {
        "mount_point": "",
        "drives": "",
        "mappings": "",
    },
}


class EWSConfiguration(Configuration):
    pass


EWSSettings = EWSConfiguration(
    config_path=os.environ.get("EWS_CONFIG_PATH", Path.home()),
    config_file_name=os.environ.get("EWS_CONFIG_FILENAME", ".ews_config"),
    defaults=default_config,
    env_prefix="EWS",
)
