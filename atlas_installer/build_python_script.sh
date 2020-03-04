#!/bin/bash

source build_tools/get.sh

mkdir -p dist \
    && echo "Building python script..." \
    && sed "s/There is no version information available./$(get_version)/g" \
        atlas_installer.py > dist/atlas_installer_before_license.py \
    && tar -zcvf licenses.tgz licenses \
    && sed "s/This is the license tar byte string used by the builder do not remove/$(python print_license_tar_bye_string.py)/g" \
        dist/atlas_installer_before_license.py > dist/atlas_installer.py \
    && rm licenses.tgz dist/atlas_installer_before_license.py \
    && echo "Finished python script"

du -hs dist/*