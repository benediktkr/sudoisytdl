#!/bin/bash

set -e

docker build --build-arg UID=1000 -t benediktkr/sudoisytdl:latest .

env_file="./dev.env"
source ${env_file}

mkdir -p ${DL_DIR_HOST}
chown -R 1000:1000 ${DL_DIR_HOST}

mkdir -p ${WEB_DIR_HOST}
chown -R 1000:1000 ${WEB_DIR_HOST}

mkdir -p dist/
chown -R 1000:1000 dist/

if [ "$1" = "dl" ] || [ "$1" = "tg" ] || [ "$1" = "--debug" ]; then
    CMD="run ytdl $@"
elif [ "$1" = "version" ] && [ ! -z "$2" ]; then
    CMD=$@
    sed -i "s/__version__.*/__version__ = '$2'/g" sudoisytdl/__init__.py

else
    CMD=$@

fi

docker run \
       -v ${WEB_DIR_HOST}:${WEB_DIR} \
       -v ${DL_DIR_HOST}:${DL_DIR} \
       --env-file ${env_file} \
       --name sudoisytdl \
       --rm -it benediktkr/sudoisytdl:latest $CMD

       # -v $(pwd)/pyproject.toml:/sudois/pyproject.toml \
       # -v $(pwd)/poetry.lock:/sudois/poetry.lock \
       # -v $(pwd)/sudoisytdl:/sudois/sudoisytdl \
       # -v $(pwd)/dist:/sudois/dist \
