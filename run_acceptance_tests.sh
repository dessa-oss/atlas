#!/bin/bash


cd testing

for acceptance_directory in $(echo *acceptance)
do
    if [[ $acceptance_directory != "scheduler_acceptance" && $acceptance_directory != "orbit_acceptance" ]]
    then
        python -Wi -m unittest -f -v $acceptance_directory || exit 1
    else
        echo "SKIPPING ALL SCHEDULER ACCEPTANCE TESTS FOR NOW DUE TO CONFIG TRANSLATE CONFLICTS"
        echo "THE 'scheduler' CONFIG ENV POINTS TO THE LOCAL DOCKER SCHEDULER PLUGIN TRANSLATE"
    fi
done

# TODO: Fix tensorboard first
# cd ../tensorboard
# for acceptance_directory in $(echo *acceptance)
# do
#     python -Wi -m unittest -f -v $acceptance_directory || exit 1
# done