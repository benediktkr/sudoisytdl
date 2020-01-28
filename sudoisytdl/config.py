import os

DL_DIR = os.environ.get("DL_DIR", "/data")
WEB_DIR = os.environ.get("WEB_DIR", "/web")
DOMAIN = os.environ["DOMAIN"]

TG_TOKEN = os.environ["TG_TOKEN"]
MY_TG = os.environ["MY_TG"]

DEFAULT_LOG_LEVEL = "INFO"

_debug_env = os.environ.get("DEBUG", "False")
DEBUG = _debug_env.lower() == "true"

LOG_FILE = os.path.join(DL_DIR, "sudoisytdl.log")
