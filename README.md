# sudoisytdl

[![Build Status](https://jenkins.sudo.is/buildStatus/icon?job=ben%2Fsudoisytdl%2Fmaster&style=flat-square)](https://jenkins.sudo.is/job/ben/job/sudoisytdl/job/master/)
![Docker Image Version (latest by date)](https://img.shields.io/docker/v/benediktkr/sudoisytdl?style=flat-square)

A simple Telegram bot made with [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) and [youtube-dl](https://youtube-dl.org/) to download YouTube videos.

This was a weekend hack project.

The Telegram API doesn't allow for uploading files larger than 50MB, so this will copy the file to a webserver and send the user a link that expires after 60 minutes. The link has a SHA-256 hash of the filename and Telegram username, and the web server should disallow file listing (and set a robots.txt to disallow search engines as well). Given that the links only live for 60 minutes, this should be sufficient.


Upstream repo: [git.sudo.is/ben/sudoisytdl](https://git.sudo.is/ben/sudoisytdl)

GitHub mirror: [github.com/benediktkr/sudoisytdl](https://github.com/benediktkr/sudoisytdl).
