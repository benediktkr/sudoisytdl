#!/usr/bin/env python3

import hashlib
from shutil import copyfile, rmtree
from os import path, makedirs, stat, listdir
from datetime import datetime
from urllib.parse import quote

from loguru import logger

from sudoisytdl import config

def get_digest(filepath):
    m = hashlib.sha256()
    m.update(filepath.encode())
    digest = m.hexdigest()

    return digest

def copy_to_webdir(src):
    filename = path.split(src)[-1]
    digest = get_digest(src)

    dest_dir = path.join(config.WEB_DIR, digest)
    dest = path.join(dest_dir, filename)

    makedirs(dest_dir, exist_ok=True)
    copyfile(src, dest)

    url = "/".join(["https:/", config.DOMAIN, digest, quote(filename)])
    logger.debug(f"copied '{filename}' to '{url}'")
    return url

def remove_expired_from_webdir(max_mins=90):
    ls = listdir(config.WEB_DIR)
    files = [path.join(config.WEB_DIR, a) for a in ls if a != "robots.txt"]
    now = datetime.now()
    for item in files:
        mtime = datetime.fromtimestamp(stat(item).st_mtime)
        age = now - mtime
        minutes = age.total_seconds() // 60
        if minutes > max_mins:
            rmtree(item)
            logger.info(f"expired {item}")
        # else:
        #     logger.debug(f"{item}: {minutes}mins")
