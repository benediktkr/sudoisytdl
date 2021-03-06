#!/usr/bin/env python3

import argparse
import sys

from loguru import logger

from sudoisytdl import config
from sudoisytdl import __version__
from sudoisytdl import yt
from sudoisytdl import tg

def run_dl(args):
    filenames = yt.download(args.url, args.force_download)
    for k, v in filenames.items():
        logger.success(f"{k}: '{v}")

def run_tg(args):
    tg.start_bot()

def run_version(args):
    print(__version__)

def cli():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--debug", action="store_true")
    subparsers = parser.add_subparsers(dest='cmd')
    subparsers.required = True

    parser_version = subparsers.add_parser('version', help="print version")
    parser_version.set_defaults(func=run_version)

    parser_dl = subparsers.add_parser('dl', help="download with youtube-dl")
    parser_dl.add_argument('--url', help="youtube url", required=True)
    parser_dl.add_argument("--force-download", action="store_true",
                           help="download and overwrite file if exists")
    parser_dl.set_defaults(func=run_dl)

    parser_tg = subparsers.add_parser('tg', help="start telegram bot")
    parser_tg.set_defaults(func=run_tg)

    args = parser.parse_args()

    if not args.debug or config.DEBUG:
        logger.remove()
        logger.add(sys.stderr, level=config.DEFAULT_LOG_LEVEL)
    else:
        logger.warning("debug mode enabled")

    logger.add(config.LOG_FILE, level=config.DEFAULT_LOG_LEVEL)

    logger.info(f'sudoisytdl v{__version__}')

    return args.func(args)

def main():
    with logger.catch():
        cli()
