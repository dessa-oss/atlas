#!/bin/bash

FOUNDATIONS_HOME=${FOUNDATIONS_HOME:-$(realpath ~)/.foundations}
TRACKER_NAME=${TRACKER_NAME:-"foundations-tracker"}
network_name="foundations"

if [ -z "$1" ];then
    echo "No product specified, using default of ${network_name}"
else
    export network_name="${network_name}-$1"
fi

if [ -z "$2" ]; then
    REDIS_PORT=6379
else
    REDIS_PORT=$2
fi

echo "Creating network ${network_name}"
docker network create -d bridge $network_name > /dev/null 2>&1 || true

redis_container_id=$(docker ps --filter "name=${TRACKER_NAME}" -q)
if [ -z "$redis_container_id" ]; then
    echo "Creating redis container at redis://${TRACKER_NAME}:${REDIS_PORT}"
    mkdir -p $FOUNDATIONS_HOME/database \
        && docker run \
            --rm \
            --name $TRACKER_NAME \
            -p $REDIS_PORT:6379 \
            --network=$network_name \
            --volume $FOUNDATIONS_HOME/database:/data \
            -d redis redis-server --appendonly yes
else
    echo "Connecting existing REDIS ${TRACKER_NAME} to network ${network_name}"
    docker network connect $network_name $redis_container_id --alias $TRACKER_NAME > /dev/null 2>&1 || true
fi