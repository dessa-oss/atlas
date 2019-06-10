#!/bin/bash

python -m pip install setuptools_scm docker

pip_version=`foundations_contrib/src/foundations_contrib/resources/get_version.sh`
export build_version=`echo $pip_version | sed 's/+/_/g'`

if [ $? -eq 0 ]
then
    python push_gui_images.py
fi
