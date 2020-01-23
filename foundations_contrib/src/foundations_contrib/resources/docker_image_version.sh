#!/bin/bash

pip_version=$(python -c 'import foundations_internal.versioning;print(foundations_internal.versioning.__version__)')
echo $pip_version | sed 's/+/_/g'