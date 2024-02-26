import logging
import os
from pathlib import Path

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
    "pypi": {
        "username": "__token__",
        "token": "",
        "password": "",
    },
    "testpypi": {
        "username": "__token__",
        "token": "",
        "password": "",
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
