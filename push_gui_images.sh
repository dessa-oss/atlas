#!/bin/bash

python -m pip install setuptools_scm docker

export build_version=`python get_version.py | sed 's/+/_/g'`

if [ $? -eq 0 ]
then
    python push_gui_images.py
fi
