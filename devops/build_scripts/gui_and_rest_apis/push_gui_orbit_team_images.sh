#!/bin/bash

export PACKAGE_NAME=${PACKAGE_NAME:-orbit-team-dev}

# convert the NEXUS_DOCKER_REGISTRY to the project specific domain if not converted before
if [[ $NEXUS_DOCKER_REGISTRY != *"$PACKAGE_NAME"* ]]; then
  export NEXUS_DOCKER_REGISTRY="$NEXUS_DOCKER_REGISTRY/$PACKAGE_NAME"
fi

python -m pip install setuptools_scm docker

pip_version=`python get_version.py`
export build_version=`echo $pip_version | sed 's/+/_/g'`
script_location="`pwd`/devops/build_scripts"

if [ $? -eq 0 ]
then
   python $script_location/gui_and_rest_apis/push_gui_orbit_team_images.py
fi
