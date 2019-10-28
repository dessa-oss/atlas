#!/bin/bash

python -m pip install setuptools_scm docker

pip_version=`foundations_contrib/src/foundations_contrib/resources/get_version.sh`
export build_version=`echo $pip_version | sed 's/+/_/g'`


if [ $? -eq 0 ]
then
    rm -rf tmp/pip_wheels && \
        mkdir -p tmp/pip_wheels && \
        pip download --dest tmp/pip_wheels dessa_foundations==$pip_version && \
        pip download --dest tmp/pip_wheels foundations-core_rest_api_components==$pip_version && \
        pip download --dest tmp/pip_wheels foundations-rest-api==$pip_version && \
        pip download --dest tmp/pip_wheels foundations-orbit-rest-api==$pip_version && \
        pip download --dest tmp/pip_wheels foundations_orbit==$pip_version && \
        python build_gui_orbit_team.py
fi