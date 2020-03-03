#!/bin/bash

gui_docker_image="foundations-gui"
docker_registry="docker.shehanigans.net"
pip_build_version=`python get_version.py`
docker_build_version=$(echo $pip_build_version | sed 's/+/_/g')

gui_image_tag=${docker_registry}/${gui_docker_image}:${docker_build_version}

docker build -t ${gui_image_tag} --network=host foundations_ui