#!/bin/bash

function get_coverage_report_for_module {
    module_directory="$1"
    real_module_name="$2"
    coverage_type="$3"

    if [ -d "${module_directory}/test" ] && { [ "${coverage_type}" == "unittest" ] || [ "${coverage_type}" == "all" ]; }; then
        echo "Running coverage for unit tests"
        cd "${module_directory}" || exit && \
            coverage run --source="${real_module_name}" -m unittest test
    fi
    if [ -d "${module_directory}/integration" ]  && { [ "${coverage_type}" == "integration" ] || [ "${coverage_type}" == "all" ]; }; then
        echo "Running coverage for integration tests"
        cd "${module_directory}" || exit && \
            coverage run --source="${real_module_name}" -m unittest integration
    fi
    if [ -d "${module_directory}/test" ] || [ -d "${module_directory}/integration" ]; then
        coverage html -i && \
        mkdir -p "${cwd}/atlas/coverage_results" && \
        cp .coverage "${cwd}/atlas/coverage_results/.coverage_${real_module_name}"
    fi
}

cwd=$(pwd)

if [ -z "$1" ]; then
  coverage_type="all"
else
  coverage_type=$1
fi

export TZ=EST

for module_directory in $(echo atlas/foundations_*) $(echo atlas/*_utils)
do
    real_module_name=$(basename "$module_directory")

    if [[ "$module_directory" == "atlas/foundations_sdk" ]]; then
        real_module_name="foundations"
    fi
    
    if [[ "$module_directory" == "atlas/gcp_utils" ]]; then
        real_module_name="foundations_gcp"
    fi
    
    if [[ "$module_directory" == "atlas/aws_utils" ]]; then
        real_module_name="foundations_aws"
    fi

    get_coverage_report_for_module "${cwd}/${module_directory}/src" ${real_module_name} "${coverage_type}"
done

cd ${cwd}/atlas/coverage_results && \
coverage combine .coverage* && \
coverage html -i