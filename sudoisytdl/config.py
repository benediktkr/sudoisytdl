import os

DL_DIR = os.environ["DL_DIR"]
TG_TOKEN = os.environ["TG_TOKEN"]
WEB_DIR = os.environ["WEB_DIR"]
DOMAIN = os.environ["DOMAIN"]
MY_TG = os.environ["MY_TG"]

_debug = os.environ.get("DEBUG", "False")
DEBUG = _debug.lower() == "true"
