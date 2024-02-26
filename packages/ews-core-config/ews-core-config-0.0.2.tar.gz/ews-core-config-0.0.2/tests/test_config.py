import os

from ews_core_config import EWSSettings


def test_config():
    settings = EWSSettings.get_settings()
    # pprint(settings)
    envs = {k: v for k, v in os.environ.items() if k.startswith("EWS_")}
    assert envs
    # pprint(envs)
