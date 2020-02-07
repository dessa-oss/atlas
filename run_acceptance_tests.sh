#!/bin/bash

CWD=$(pwd)

source ./devops/set_environment_for_docker_scheduler.sh
./devops/startup_frontend_dev_atlas.sh

echo "Waiting for Atlas GUI to start at http://localhost:3000"
./devops/build_scripts/helpers/wait_for_url.sh "http://localhost:3000" 80


cd "$CWD/testing" || exit

for acceptance_directory in $(echo *acceptance)
do
    if [[ $acceptance_directory != "orbit_acceptance" ]]
    then
        python -Wi -m unittest -f -v $acceptance_directory || exit 1
    else
        echo "SKIPPING ALL SCHEDULER ACCEPTANCE TESTS FOR NOW DUE TO CONFIG TRANSLATE CONFLICTS"
        echo "THE 'scheduler' CONFIG ENV POINTS TO THE LOCAL DOCKER SCHEDULER PLUGIN TRANSLATE"
    fi
done

cd "$CWD/foundations_rest_api/src" || exit
python -Wi -m unittest -f -v acceptance || exit 1

cd $CWD

echo "Running Orbit Acceptance test"
./devops/startup_frontend_dev_orbit.sh

echo "Waiting for Atlas Orbit to start at http://localhost:3000"
./devops/build_scripts/helpers/wait_for_url.sh "http://localhost:3000" 80

cd "$CWD/testing" || exit
python -Wi -m unittest -f -v orbit_acceptance || exit 1

cd $CWD

./devops/teardown_frontend_dev_atlas.sh
./devops/teardown_frontend_dev_orbit.sh

# TODO: Fix tensorboard first
# cd ../tensorboard
# for acceptance_directory in $(echo *acceptance)
# do
#     python -Wi -m unittest -f -v $acceptance_directory || exit 1
# done