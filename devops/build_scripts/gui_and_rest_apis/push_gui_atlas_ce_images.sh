#!/bin/bash

python -m pip install setuptools_scm docker

pip_version=`python get_version.py`
export build_version=`echo $pip_version | sed 's/+/_/g'`
script_location="`pwd`/devops/build_scripts"

if [ $? -eq 0 ]
then
    python $script_location/gui_and_rest_apis/push_gui_images.py
fi
