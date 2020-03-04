#!/bin/bash

GET_PWD=$(pwd)

get () {
    local CWD=$(pwd)
    cd $GET_PWD \
        && echo $(python get_field.py $VERSION_FILE $1)
    cd $CWD
}

get_version () {
    local CWD=$(pwd)
    local DEST=$CWD
    if [[ -n $1 ]]; then
        DEST=$1
    fi
    cd $DEST
    echo $(python -c 'from setuptools_scm import get_version; print(get_version())' | sed 's/+/_/g')
    cd $CWD
}