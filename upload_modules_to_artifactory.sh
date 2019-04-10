#!/bin/bash
cwd=`pwd`
echo $NEXUS_USER

twine upload -u jenkins-user -p $NEXUS_PASSWORD --repository-url $NEXUS_URL ${cwd}/dist/*.whl