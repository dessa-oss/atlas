#!/bin/bash

if [[ $# -ne 1 ]]
then
    echo "USAGE: $0 <nexus_url>"
else
    nexus_url="$1"
fi

cwd=`pwd`
echo Uploading modules via user $NEXUS_USER

twine upload -u $NEXUS_USER -p $NEXUS_PASSWORD --repository-url ${nexus_url} ${cwd}/dist/*.whl