#!/usr/bin/env python3

from __future__ import unicode_literals
import os

from loguru import logger
import youtube_dl

from sudoisytdl import config
from youtube_dl.utils import DownloadError

def my_hook(d):
    if d['status'] == 'finished':
        logger.info('Done downloading, now converting ...')

def download(url, dlmode, force=True, username="local"):

    archive_file = os.path.join(config.DL_DIR, "archive.txt")
    os.makedirs(os.path.join(config.DL_DIR, username), exist_ok=True)
    ydl_opts = {
        # try just "bestvideo+bestaudio"
        'format': "bestvideo[ext=mkv]+bestaudio[ext=mp3]/bestvideo+bestaudio",
        #'format': "bestvideo+bestaudio",
        'noplaylist': True,
        'download_archive': "/dev/null",
        'outtmpl': os.path.join(config.DL_DIR, username, '%(title)s.%(ext)s'),
        'logger': logger,
        'progress_hooks': [my_hook],
        'keepvideo': True
    }
    if dlmode in ["audio", "both"]:
        ydl_opts["postprocessors"] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }]
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        filename_base = ydl.prepare_filename(info)
        if os.path.exists(filename_base) and not force:
            logger.warning(f"'{filename_base}' already exists, skipping")
        else:
            res = ydl.download([url])
            logger.info(f"downloaded '{filename_base}'")

    noext = os.path.splitext(filename_base)[0]
    filename_mkv = noext + ".mkv"
    if os.path.exists(filename_base):
        filename_video = filename_base
    elif os.path.exists(filename_mkv):
        filename_video = filename_mkv
    else:
        raise DownloadError("video file missing")

    filename_audio = noext + ".mp3"

    if dlmode == "both":
        files = {
            'audio': filename_audio,
            'video': filename_video
        }
    elif dlmode == "audio":
        files = {'audio': filename_audio}
    else:
        files = {'video': filename_video}

    name = noext.split("/")[-1]
    return {'name': name,
            'files': files}
