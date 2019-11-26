function get_coverage_report_for_module {
    module_directory_to_add="$1"
    module_directory="$2"
    if [ -d "${module_directory_to_add}/test" ]; then
        cd ${module_directory_to_add}
        coverage run --source=./${module_directory} -m unittest test && \
        coverage html
    fi
}

cwd=`pwd`

export TZ=EST

for module_directory in $(echo foundations_*) $(echo *_utils)
do
    get_coverage_report_for_module "${cwd}/${module_directory}/src" ${module_directory}
done
