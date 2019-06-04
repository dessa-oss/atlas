#!/bin/bash

action="$1"

if [ "$3" = "" ]
then
    image_tag="latest"
else
    image_tag="$3"
fi

if [ "$FOUNDATIONS_GUI_PORT" = "" ]; then
    FOUNDATIONS_GUI_PORT=6443
fi

get_redis_container_image () {
    docker ps --format "{{.Image}}" | grep -E '^redis:?.*$' | head -n1
}

create_redis_if_not_exists () {
    if [[ -z "$(get_redis_container_image)" ]]; then
        echo "Creating redis."
        docker run -d --rm \
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

    echo "Starting Foundations UI..."

    docker run -d --rm \
        --name foundations-rest-api \
        -e REDIS_URL="${redis_url}" \
        --network foundations-gui \
        docker.shehanigans.net/foundations-rest-api:${image_tag} \
        > /dev/null \
        && \

    docker run -d --rm \
        --name foundations-gui \
        -e FOUNDATIONS_REST_API=foundations-rest-api \
        --network foundations-gui \
        -p $FOUNDATIONS_GUI_PORT:6443 \
        docker.shehanigans.net/foundations-gui:${image_tag} \
        > /dev/null \
        && \

    echo "Foundations UI listening on port $FOUNDATIONS_GUI_PORT."
}

stop_ui () {
    echo "Stopping Foundations UI..."

    docker stop foundations-gui > /dev/null
    gui_stop=$?

    docker stop foundations-rest-api > /dev/null
    rest_api_stop=$?

    if [ ${gui_stop} -eq 0 ] && [ ${rest_api_stop} -eq 0 ]
    then
        echo "Foundations UI stopped."
    fi
}

if [ "${action}" = "start" ]
then
    start_ui || stop_ui
elif [ "${action}" = "stop" ]
then
    stop_ui
else
    echo "USAGE: $0 <start|stop> ui [image_tag]"
    echo "image_tag is optional; omit to use 'latest'"
    exit 1
fi