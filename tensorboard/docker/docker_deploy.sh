# Usage: ./docker_deploy.sh <repo> <tag> <archive_mount> <logdir_mount> <tb_port>

repo=${1:-docker.shehanigans.net}
tag=${2:-latest}
archive=${3:-archive}
logdir=${4:-logs}
tb_port=${5:-6006}

./tensorboard_rest_api/build_image.sh $repo $tag && \
./tensorboard_server/build_image.sh $repo $tag && \

docker run --rm -d \
    -p 5000:5000 \
    -v $(realpath $archive):/archive \
    -v $(realpath $logdir):/logs \
    $repo/tensorboard-rest-api:$tag \
    python /app/tensorboard_rest_api_server.py 5000 False && \

docker run --rm -d \
    -p $tb_port:$tb_port \
    -v $(realpath $archive):/archive \
    -v $(realpath $logdir):/logs \
    $repo/tensorboard-server:$tag \
    tensorboard --logdir /logs

