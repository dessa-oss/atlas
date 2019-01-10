#!/bin/bash

node_ip="192.168.0.21"
redis_url="redis://192.168.0.21:6379"

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
        -p 37722:37722 \
        foundations-rest-api:${image_tag} \
        > /dev/null \
        && \

    docker run -d --rm \
        --name foundations-gui \
        -e FOUNDATIONS_REST_API="${node_ip}:37722" \
        -p 3000:3000 \
        foundations-gui:${image_tag} \
        > /dev/null \
        && \

    echo "Foundations UI listening on port 3000."
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