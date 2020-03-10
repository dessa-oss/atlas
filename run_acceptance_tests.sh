#!/bin/bash

CWD=$(pwd)


cd "$CWD/atlas/testing" || exit

for acceptance_directory in $(echo *acceptance)
do
    python -Wi -m unittest -f -v $acceptance_directory || exit 1
done

cd "$CWD/atlas/foundations_rest_api/src" || exit
python -Wi -m unittest -f -v acceptance || exit 1


# TODO: Fix tensorboard first
# cd ../tensorboard
# for acceptance_directory in $(echo *acceptance)
# do
#     python -Wi -m unittest -f -v $acceptance_directory || exit 1
# done