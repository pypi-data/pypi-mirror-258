import os

from ews_core_config import EWSSettings


def test_config():
    settings = EWSSettings.get_settings()
    envs = {k: v for k, v in os.environ.items() if k.startswith("EWS_")}
    assert envs


def test_user_file_read():
    settings = EWSSettings.get_settings()
    assert EWSSettings.pypi_username != ""
