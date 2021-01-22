#!/usr/bin/env python3

import argparse
import sys

from loguru import logger

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
    subparser = parser.add_subparsers()

    parser_dl = subparser.add_parser('dl')
    parser_dl.add_argument('url')
    parser_dl.add_argument("--force", action="store_true")
    parser_dl.set_defaults(func=dl)

    parser_tg = subparser.add_parser('tg')
    parser_tg.set_defaults(func=run_tg)

    args = parser.parse_args()

    if not args.debug:
        logger.remove()
        logger.add(sys.stderr, level="SUCCESS")

    args.func(args)
