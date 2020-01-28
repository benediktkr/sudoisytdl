#!/usr/bin/env python3

import argparse
import sys

from loguru import logger

from sudoisytdl import config
from sudoisytdl import yt
from sudoisytdl import tg


def dl(args):
    filenames = yt.run_download(args)
    for k, v in filenames.items():
        logger.success(f"{k}: '{v}")

def run_tg(args):
    tg.start_bot(args)

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--debug", action="store_true")
    subparsers = parser.add_subparsers(dest='cmd')
    subparsers.required = True

    parser_dl = subparsers.add_parser('dl', help="download with youtube-dl")
    parser_dl.add_argument('url', help="youtube url")
    parser_dl.add_argument("--force-download", action="store_true",
                           help="download and overwrite file if exists")
    parser_dl.set_defaults(func=dl)

    parser_tg = subparsers.add_parser('tg', help="start telegram bot")
    parser_tg.set_defaults(func=run_tg)

    args = parser.parse_args()

    if not args.debug or config.DEBUG:
        logger.remove()
        logger.add(sys.stderr, level=config.DEFAULT_LOG_LEVEL)
    else:
        logger.warning("debug mode enabled")

    logger.add(config.LOG_FILE, level=config.DEFAULT_LOG_LEVEL)

    args.func(args)
