#!/bin/bash

pip_version=`./get_version.sh`
echo $pip_version | sed 's/+/_/g'