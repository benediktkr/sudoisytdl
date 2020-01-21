#!/usr/bin/env python3

from __future__ import unicode_literals
import os

from loguru import logger
import youtube_dl

def my_hook(d):
    logger.info(d)
    if d['status'] == 'finished':
        logger.info('Done downloading, now converting ...')

def download_audio(yt_url):
    ydl_opts = {
        'format': 'bestaudio/best',

        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': logger,
        'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        res = ydl.download([yt_url])
        logger.debug(res)
