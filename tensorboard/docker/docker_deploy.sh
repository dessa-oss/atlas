# Usage: ./docker_deploy.sh <repo> <tag> <archive_mount> <logdir_mount> <tb_port>

NEXUS_DOCKER_REGISTRY=${1:-docker.shehanigans.net}
build_version=${2:-latest}
archive=${3:-archive}
logdir=${4:-logs}
tb_port=${5:-6006}

./tensorboard_rest_api/build_image.sh $NEXUS_DOCKER_REGISTRY $build_version && \
./tensorboard_server/build_image.sh $NEXUS_DOCKER_REGISTRY $build_version && \

docker run --rm -d \
    -p 5000:5000 \
    -v $(realpath $archive):/archive \
    -v $(realpath $logdir):/logs \
    --name tensorboard-rest-api \
    $NEXUS_DOCKER_REGISTRY/tensorboard-rest-api:$build_version \
    python /app/tensorboard_rest_api_server.py 5000 False && \

docker run --rm -d \
    -p $tb_port:$tb_port \
    -v $(realpath $archive):/archive \
    -v $(realpath $logdir):/logs \
    --name tensorboard-server \
    $NEXUS_DOCKER_REGISTRY/tensorboard-server:$build_version \
    tensorboard --logdir /logs

