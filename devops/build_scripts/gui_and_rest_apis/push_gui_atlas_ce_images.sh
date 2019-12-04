#!/bin/bash

python -m pip install setuptools_scm docker

script_location="$(pwd)/devops/build_scripts"
source "$script_location/build_common.sh"

if [ $? -eq 0 ]
then
    python $script_location/gui_and_rest_apis/push_gui_images.py
fi
