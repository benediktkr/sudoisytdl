#!/bin/bash

set -e

./build.sh

env_file="./dev.env"
source ${env_file}

docker run -v ${WEB_DIR_HOST}:${WEB_DIR} -v ${DL_DIR_HOST}:${DL_DIR} --env-file ${env_file} --name sudoisytdl --rm -it benediktkr/sudoisytdl:latest $@
