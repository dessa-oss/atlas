#!/bin/bash

repo=${1:-docker.shehanigans.net}
tag=${2:-latest}

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

docker build -t $repo/tensorboard-server:$tag $DIR