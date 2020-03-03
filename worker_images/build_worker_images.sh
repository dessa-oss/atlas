#!/bin/bash


docker_registry="docker.shehanigans.net"
pip_build_version=`python get_version.py`
docker_build_version=$(echo $pip_build_version | sed 's/+/_/g')

worker_dir="$(pwd)/worker_images"

worker_image_tag=${docker_registry}/atlas-common/worker:${docker_build_version}
worker_gpu_image_tag=${docker_registry}/atlas-common/worker-gpu:${docker_build_version}

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

echo "Built worker images successfully" || echo "Failed to build worker images"