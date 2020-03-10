#!/bin/bash

export build_version=$(python get_version.py)
root_dir="$(pwd)"
base_dir="${root_dir}/atlas_installer"
working_dir="${base_dir}/dist"

rm -rf $working_dir \
    && mkdir -p $working_dir \
    && echo "Building atlas installer script..." \
    && echo "Copying the current atlas version (${build_version}) into the installer file" \
    && sed "s/There is no version information available./${build_version}/g" \
        $base_dir/atlas_installer.py > $working_dir/atlas_installer_before_notice.py \
    && echo "Compressing the notice into a tar file" \
    && tar -zcvf $working_dir/licenses.tgz NOTICE.md > /dev/null 2>&1 \
    && sed "s/This is the license tar byte string used by the builder do not remove/$(python $base_dir/print_license_tar_bye_string.py $working_dir/licenses.tgz)/g" \
        $working_dir/atlas_installer_before_notice.py > $working_dir/atlas_installer.py \
    && echo "Cleaning up intermediary artifacts" \
    && rm $working_dir/licenses.tgz $working_dir/atlas_installer_before_notice.py \
    && echo "Finished building atlas installer script"