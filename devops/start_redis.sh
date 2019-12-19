#!/bin/bash

FOUNDATIONS_HOME=${FOUNDATIONS_HOME:-$(realpath ~)/.foundations}

network_name="foundations"
if [ -z "$1" ];then
    echo "No product specified, using default of ${network_name}"
else
    network_name="${network_name}-$1"
fi

if [ -z "$2" ]; then
    redis_port=6379
else
    redis_port=$2
fi

echo "Creating network ${network_name}"
docker network create -d bridge $network_name >/dev/null 2>&1 || true

redis_container_id=$(docker ps --filter "name=redis" -q)
if [ -z "$redis_container_id" ]; then
    echo "Creating redis container at port ${redis_port}"
    mkdir -p $FOUNDATIONS_HOME/database \
        && docker run \
            --rm \
            --name redis \
            -p 6379:$redis_port \
            --network=$network_name \
            --volume $FOUNDATIONS_HOME/database:/data \
            -d redis redis-server --appendonly yes
else
    docker network connect $network_name $redis_container_id --alias redis
fi