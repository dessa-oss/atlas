#!/bin/bash

action="$1"

if [ "$4" = "" ]; then
    image_tag=`./docker_image_version.sh`
else
    image_tag="$4"
fi

image_name="$3"

if [ "$FOUNDATIONS_GUI_PORT" = "" ]; then
    FOUNDATIONS_GUI_PORT=6443
fi

get_redis_container_image () {
    docker ps --format "{{.Image}}" | grep -E '^redis:?.*$' | head -n1
}

create_redis_if_not_exists () {
    if [[ -z "$(get_redis_container_image)" ]]; then
        echo "Creating redis."
        docker run -d \
            --restart always \
            --name foundations-redis \
            -p 6379:6379 \
            redis:5 \
            > /dev/null

        if [[ $? -ne 0 ]]; then
            echo "Failed to start redis."
            exit 1
        fi
    fi
}

create_network_if_not_exists () {
    if [[ -z "$(docker network ls --filter name=foundations-gui --format \"{{.ID}}\")" ]]; then
        docker network create -d bridge foundations-gui
    fi
}

start_ui () {
    create_network_if_not_exists

    if [[ ! -z "${REDIS_URL}" ]]; then
        echo "Using redis at ${REDIS_URL}"
        redis_url=$REDIS_URL
        rest_api_link_option=""
    else
        echo "Redis url not set."

        create_redis_if_not_exists

        redis_container_image=$(get_redis_container_image)
        redis_container_name=$(docker ps -f ancestor=${redis_container_image} --format "{{.Names}}" | head -n1)

        docker network connect foundations-gui ${redis_container_name} 2> /dev/null

        echo "Using redis container ${redis_container_name}"

        redis_url="redis://${redis_container_name}:6379"
    fi

    echo "Starting ${image_name} UI..."

    docker run -d \
        --restart always \
        --name ${image_name}-rest-api \
        -e REDIS_URL="${redis_url}" \
        -e FOUNDATIONS_ARCHIVE_HOST="${FOUNDATIONS_ARCHIVE_HOST}" \
        --network foundations-gui \
        -v $HOME/.kube:/root/.kube:ro \
        docker.shehanigans.net/${image_name}-rest-api:${image_tag} \
        > /dev/null \
        && \

    docker run -d \
        --restart always \
        --name ${image_name}-gui \
        -e FOUNDATIONS_REST_API=${image_name}-rest-api \
        --network foundations-gui \
        -p $FOUNDATIONS_GUI_PORT:6443 \
        docker.shehanigans.net/${image_name}-gui:${image_tag} \
        > /dev/null \
        && \

    echo "${image_name} UI listening on port $FOUNDATIONS_GUI_PORT."
}

stop_ui () {
    echo "Stopping ${image_name} UI..." && \
        docker stop ${image_name}-gui 2>&1 > /dev/null && \
        docker rm ${image_name}-gui 2>&1 > /dev/null && \
        echo "${image_name} UI stopped." || echo "Unable to stop ${image_name} UI"
        docker stop ${image_name}-rest-api 2>&1 > /dev/null && \
        docker rm ${image_name}-rest-api 2>&1 > /dev/null && \
        echo "${image_name} REST API stopped." || echo "Unable to stop ${image_name} REST API"
}

if [ "${action}" = "start" ]
then
    start_ui || stop_ui
elif [ "${action}" = "stop" ]
then
    stop_ui
else
    echo "USAGE: $0 <start|stop> ui <foundations|foundations-orbit> [image_tag]"
    echo "image_tag is optional; omit to use 'latest'"
    exit 1
fi