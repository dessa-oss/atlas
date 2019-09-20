#!/bin/bash

wheel_suffix=`python -c "import sys; print(sys.version_info.major)"`

python -m pip install setuptools_scm
export build_version=`python get_version.py`

wheel_name_tail="${build_version}-py${wheel_suffix}-none-any.whl"

download_pytransform_files () {
    cd $1 && \
#        wget http://pyarmor.dashingsoft.com/downloads/platforms/win32/_pytransform.dll && \
#        wget http://pyarmor.dashingsoft.com/downloads/platforms/win_amd64/_pytransform.dll && \
#        wget http://pyarmor.dashingsoft.com/downloads/platforms/linux_i386/_pytransform.so && \
        wget http://pyarmor.dashingsoft.com/downloads/platforms/linux_x86_64/_pytransform.so && \
#        wget http://pyarmor.dashingsoft.com/downloads/platforms/macosx_x86_64/_pytransform.dylib && \
        cd -
}

obfuscate_modules () {
    src_module_path=$1
    dest_module_path=$2

    echo "Obfuscating ${src_module_path} into ${dest_module_path}" && \
        echo `pwd`
        mkdir -p obi && \
        rm -rf ${dest_module_path}/* && \
        pyarmor obfuscate --output=${dest_module_path} -r ${src_module_path}/__init__.py && \
        download_pytransform_files ${dest_module_path}
}

build_module () {
    directory=$1
    module_name=$2
    cwd=$3
    module_name_in_src=$4
    obfuscation_source_path=src/${module_name_in_src}
    obfuscation_dest_path=obfuscated_dist/${module_name_in_src}
    wheel_path=${directory}/dist/${module_name}-${wheel_name_tail}

    cd ${directory} && \
        obfuscate_modules ${obfuscation_source_path} ${obfuscation_dest_path} && \
        BUILD_FOUNDATIONS_OBFUSCATED=True python setup.py sdist bdist_wheel && \
        cd .. && \
        python -m pip install -U ${wheel_path} && \
        mkdir -p ${cwd}/dist 2>/dev/null && \
        cp $wheel_path ${cwd}/dist
}

cwd=`pwd`

rm -rf obi/* && \
    build_module foundations_internal foundations_internal ${cwd} "foundations_internal" && \
    build_module foundations_events foundations_events ${cwd} "foundations_events" && \
    build_module foundations_contrib foundations_contrib ${cwd} "foundations_contrib" && \
    build_module foundations_local_docker_scheduler_plugin foundations_local_docker_scheduler_plugin ${cwd} "foundations_local_docker_scheduler_plugin" && \
    build_module foundations_sdk dessa_foundations ${cwd} "foundations" && \
    build_module foundations_core_rest_api_components foundations_core_rest_api_components ${cwd} "foundations_core_rest_api_components" && \
    build_module foundations_rest_api foundations_rest_api ${cwd} "foundations_rest_api"