#!/bin/bash

deactivate 2> /dev/null

# make sure to add a space after module name
modules=""
modules+="cache "
modules+="grid_search "
modules+="impute_data "
modules+="loading_data "
modules+="local_cache "
modules+="logistic_regression "
modules+="one_hot_encode "
modules+="replacing_nulls "
modules+="fetch_job_information "
modules+="fetch_results "

cleanup () {
    deactivate
    rm -rf /tmp/examples-venv
    rm -rf /tmp/foundations_example*
}

cleanup_and_exit () {
    cleanup
    exit 1
}

trap 'cleanup_and_exit' SIGINT SIGTERM

for python_version in python python3
do
    rm -rf /tmp/archives

    python -m virtualenv -p ${python_version} /tmp/examples-venv
    source /tmp/examples-venv/bin/activate
    python -m pip install -r requirements.txt

    bash build_dist.sh

    cd examples

    python -m pip install -r requirements.txt

    for module in ${modules}
    do
        python -Wi -m ${module} || cleanup_and_exit
    done

    cleanup

    cd ..
done
