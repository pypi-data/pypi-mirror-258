import os
from pprint import pprint

from ews_core_config import EWSSettings

pprint(EWSSettings.get_settings())
pprint({k: v for k, v in os.environ.items() if k.startswith("EWS_")})
