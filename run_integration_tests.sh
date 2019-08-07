#!/bin/bash

export TZ=EST

function run_integration_test {
    module_directory_to_add="$1"
    if [ -d "${module_directory_to_add}/integration" ]; then
        cd ${module_directory_to_add}

        if [ "${module_directory_to_add}" != "foundations_model_package" ]; then
            python -m unittest -f -v integration || exit -1
        fi
    fi
}

cwd=`pwd`

for module_directory in $(echo foundations_*)
do
    run_integration_test "${cwd}/${module_directory}/src"
done
