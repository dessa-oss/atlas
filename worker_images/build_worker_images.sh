#!/bin/bash

docker_image="worker"
docker_registry=${DOCKER_REGISTRY:-us.gcr.io/atlas}
pip_build_version=`python get_version.py`
docker_build_version=$(echo $pip_build_version | sed 's/+/_/g')

worker_dir="$(pwd)/worker_images"

worker_image_tag=${docker_registry}/${docker_image}:${docker_build_version}
worker_image_tag_latest=${docker_registry}/${docker_image}:latest

worker_gpu_image_tag=${docker_registry}/${docker_image}-gpu:${docker_build_version}
worker_gpu_image_tag_latest=${docker_registry}/${docker_image}-gpu:latest


docker build \
    -t ${worker_image_tag} \
    --network=host \
    --file $worker_dir/tensorflow/Dockerfile \
    $worker_dir && \

docker build \
    -t ${worker_gpu_image_tag} \
    --network=host \
    --file $worker_dir/tensorflow-gpu/Dockerfile \
    $worker_dir && \

docker tag \
    $worker_image_tag \
    $worker_image_tag_latest && \

docker tag \
    $worker_gpu_image_tag \
    $worker_gpu_image_tag_latest && \

echo "Built worker images successfully"