#!/bin/bash
cwd=`pwd`
echo $NEXUS_USER

twine upload --username $NEXUS_USER --password $NEXUS_PASSWORD --repository-url $NEXUS_URL ${cwd}/dist/*.whl