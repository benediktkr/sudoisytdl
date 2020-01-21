#!/bin/bash

set -e

./build.sh

echo "args: $@"

docker run --name sudoisytdl --rm -it benediktkr/sudoisytdl:latest $@
