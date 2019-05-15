#!/bin/bash

export TZ=EST

function run_integration_test {
    module_directory_to_add="$1"
    if [ -d "${module_directory_to_add}/test" ]; then
        cd ${module_directory_to_add}
        python -m unittest -v integration || exit -1
    fi
}

cwd=`pwd`

for module_directory in $(echo foundations_*)
do
    run_integration_test "${cwd}/${module_directory}/src"
done
