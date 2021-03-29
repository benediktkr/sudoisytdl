#!/usr/bin/env python3

from __future__ import unicode_literals
import os

from loguru import logger
import youtube_dl

from sudoisytdl import config

def my_hook(d):
    if d['status'] == 'finished':
        logger.info('Done downloading, now converting ...')

def download(url, force=False, username="local"):

    archive_file = os.path.join(config.DL_DIR, "archive.txt")
    os.makedirs(os.path.join(config.DL_DIR, username), exist_ok=True)
    ydl_opts = {
        # try just "bestvideo+bestaudio"
        'format': "bestvideo[ext=mkv]+bestaudio[ext=mp3]/bestvideo+bestaudio",
        'noplaylist': True,
        'download_archive': "/dev/null",
        'outtmpl': os.path.join(config.DL_DIR, username, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'logger': logger,
        'progress_hooks': [my_hook],
        'keepvideo': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        filename_base = ydl.prepare_filename(info)
        if os.path.exists(filename_base) and not force:
            logger.warning(f"'{filename_base}' already exists, skipping")
        else:
            res = ydl.download([url])
            logger.info(f"downloaded '{filename_base}'")


    noext = os.path.splitext(filename_base)[0]
    filename_audio = noext + ".mp3"
    filename_video = noext = ".mkv"

    name = noext.split("/")[-1]
    return {'name': name,
            'files': {'audio': filename_audio,
                      'video': filename_video }}
