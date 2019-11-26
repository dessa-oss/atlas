function get_coverage_report_for_module {
    module_directory_to_add="$1"
    module_directory="$2"
    if [ -d "${module_directory_to_add}/test" ]; then
        cd ${module_directory_to_add}
        coverage erase && coverage run --source=${module_directory} -m unittest test && \
        coverage html && \
        mkdir -p ${cwd}/coverage_results && \
        cp .coverage ${cwd}/coverage_results/.coverage_${module_directory}
    fi
}

cwd=`pwd`

export TZ=EST

for module_directory in $(echo foundations_*) $(echo *_utils)
do
    if [[ "$module_directory" == "foundations_sdk" ]]; then
        real_module_name="foundations"
    fi

    if [[ "$module_directory" == "foundations_orbit_sdk" ]]; then
        real_module_name="foundations_orbit"
    fi

    if [[ "$module_directory" == "ssh_utils" ]]; then
        real_module_name="foundations_ssh"
    fi

    if [[ "$module_directory" == "gcp_utils" ]]; then
        real_module_name="foundations_gcp"
    fi

    if [[ "$module_directory" == "aws_utils" ]]; then
        real_module_name="foundations_aws"
    fi

    get_coverage_report_for_module "${cwd}/${module_directory}/src" ${real_module_name}
done

cd ${cwd}/coverage_results && \
coverage combine .coverage* && \
coverage html