#!/bin/bash

python -m pip install setuptools_scm docker

pip_version=`python get_version.py`
export build_version=`echo $pip_version | sed 's/+/_/g'`
script_location="`pwd`/devops/build_scripts"

python $script_location/workers/build_worker_images.py