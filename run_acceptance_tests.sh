#!/bin/bash

CWD=$(pwd)

source ./devops/set_environment_for_docker_scheduler.sh
./devops/startup_frontend_dev_atlas.sh

echo "Waiting for Atlas GUI to start at http://localhost:3000"
./devops/build_scripts/helpers/wait_for_url.sh "http://localhost:3000" 80


cd "$CWD/testing" || exit

for acceptance_directory in $(echo *acceptance)
do
    python -Wi -m unittest -f -v $acceptance_directory || exit 1
done

cd "$CWD/foundations_rest_api/src" || exit
python -Wi -m unittest -f -v acceptance || exit 1

cd $CWD

./devops/teardown_frontend_dev_atlas.sh

# TODO: Fix tensorboard first
# cd ../tensorboard
# for acceptance_directory in $(echo *acceptance)
# do
#     python -Wi -m unittest -f -v $acceptance_directory || exit 1
# done