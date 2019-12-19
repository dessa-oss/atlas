#!/bin/bash

FOUNDATIONS_HOME=${FOUNDATIONS_HOME:-$(realpath ~)/.foundations}

network_name="foundations"
if [ -z "$1" ];then
    echo "No product specified, using default of ${network_name}"
else
    network_name="${network_name}-$1"
fi


echo "Redis will be added to ${network_name}"

echo "docker network create -d bridge $network_name >/dev/null 2>&1 || true"
echo "mkdir -p $FOUNDATIONS_HOME/database"
echo "docker run --rm --name redis -p 6379:6379 --network=$network_name --volume $FOUNDATIONS_HOME/database:/data -d redis redis-server --appendonly yes"