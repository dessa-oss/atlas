#!/bin/bash

add_path () {
    export PYTHONPATH="$1:$PYTHONPATH"
}

cwd=`pwd`
add_path "$cwd/foundations_internal/src" && \
    add_path "$cwd/ssh_utils/src" && \
    add_path "$cwd/gcp_utils/src" && \
    add_path "$cwd/foundations_rest_api/src"