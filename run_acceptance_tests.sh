#!/bin/bash

CWD=$(pwd)

source ./devops/set_environment_for_dev.sh
./devops/startup_frontend_dev_atlas.sh

echo "Waiting for Atlas GUI to start at http://localhost:3000"
./devops/wait_for_url.sh "http://localhost:3000" 80


cd "$CWD/atlas/testing" || exit

for acceptance_directory in $(echo *acceptance)
do
    python -Wi -m unittest -f -v $acceptance_directory || exit 1
done

cd "$CWD/atlas/foundations_rest_api/src" || exit
python -Wi -m unittest -f -v acceptance || exit 1

cd $CWD

./devops/teardown_frontend_dev_atlas.sh

# TODO: Fix tensorboard first
# cd ../tensorboard
# for acceptance_directory in $(echo *acceptance)
# do
#     python -Wi -m unittest -f -v $acceptance_directory || exit 1
# done