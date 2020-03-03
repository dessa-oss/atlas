#!/bin/bash

cwd=`pwd`

if [[ $# -ne 1 ]]
then
    echo "USAGE: $0 <nexus_url>"
    exit 1
else
    nexus_url="$1"
fi


echo "Uploading modules via user $NEXUS_USER at $nexus_url"


twine upload -u $NEXUS_USER -p $NEXUS_PASSWORD --repository-url $nexus_url ${cwd}/dist/*.whl