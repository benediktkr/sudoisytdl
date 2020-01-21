#!/usr/bin/env python3

import argparse

from sudoisytdl import yt

def dl(args):
    yt.download_audio(args.yt_url)

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparser = parser.add_subparsers()
    parser_dl = subparser.add_parser('dl')
    parser_dl.add_argument('yt_url')
    parser_dl.set_defaults(func=dl)

    args = parser.parse_args()
    args.func(args)
