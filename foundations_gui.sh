#!/bin/bash

if [[ -z "${REDIS_URL}" ]]; then
    redis_url="redis://10.1.8.61:6379"
else
    redis_url=$REDIS_URL
fi

action="$1"

if [ "$3" = "" ]
then
    image_tag="latest"
else
    image_tag="$3"
fi

start_ui () {
    echo "Starting Foundations UI..."

    docker run -d --rm \
        --name foundations-rest-api \
        -e REDIS_URL="${redis_url}" \
        foundations-rest-api:${image_tag} \
        > /dev/null \
        && \

    docker run -d --rm \
        --name foundations-gui \
        -e FOUNDATIONS_REST_API=foundations-rest-api \
        --link foundations-rest-api \
        -p 6443:6443 \
        foundations-gui:${image_tag} \
        > /dev/null \
        && \

    echo "Foundations UI listening on port 6443."
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