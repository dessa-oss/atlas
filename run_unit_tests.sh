#!/bin/bash

function run_unit_test {
    module_directory_to_add="$1"
    if [ -d "${module_directory_to_add}/test" ]; then
        cd ${module_directory_to_add}
        python -m unittest -v test || exit -1
    fi
}

cwd=`pwd`

for module_directory in $(echo foundations_*) $(echo *_utils)
do
    run_unit_test "${cwd}/${module_directory}/src"
done
