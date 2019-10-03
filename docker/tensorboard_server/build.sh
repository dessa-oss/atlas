tag=${1:-latest}

docker build -t docker.shehanigans.net/tensorboard-server:$tag .