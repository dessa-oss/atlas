#!/bin/bash

# download foundations package to be included in the docker image
pip_version=`../../foundations_contrib/src/foundations_contrib/resources/get_version.sh`
export build_version=`echo $pip_version | sed 's/+/_/g'`

image_name=docker.shehanigans.net/foundations-model-package

docker push ${image_name}:${build_version}
docker push ${image_name}:latest