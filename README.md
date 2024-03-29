# sudoisytdl

[![Build Status](https://jenkins.sudo.is/buildStatus/icon?job=ben%2Fsudoisytdl%2Fmaster&style=flat-square)](https://jenkins.sudo.is/job/ben/job/sudoisytdl/job/master/)
![Docker Image Version (latest semver)](https://img.shields.io/docker/v/benediktkr/sudoisytdl?sort=semver&style=flat-square)
![Docker Image Size (latest by date)](https://img.shields.io/docker/image-size/benediktkr/sudoisytdl?sort=date&style=flat-square)


A simple Telegram bot made with [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) and [youtube-dl](https://youtube-dl.org/), to download YouTube videos. Dokerfile (and batteries) included. 

The Telegram API doesn't allow for uploading files larger than 50MB, so this will copy the file to a webserver and send the user a link that expires after 60 minutes. The link has a SHA-256 hash of the filename and Telegram username, and the web server should disallow file listing (and set a robots.txt to disallow search engines as well). The default setting is to remove the files after a time interval of 60 mins.

[Upstream repo on git.sudo.is/ben](https://git.sudo.is/ben/sudoisytdl) | [GitHub mirror](https://github.com/benediktkr/sudoisytdl).
