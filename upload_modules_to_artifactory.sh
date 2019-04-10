#!/bin/bash
cwd=`pwd`

twine upload --username $NEXUS_USER --password $NEXUS_PASSWORD --repository-url $NEXUS_URL ${cwd}/dist/*.whl