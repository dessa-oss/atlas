#!/bin/bash

source build_tools/get.sh

mkdir -p dist \
    && echo "Building python script..." \
    && sed "s/There is no version information available./$(get_version  ../../)/g" \
        atlas_installer.py > dist/atlas_installer.py \
    && echo "Finished python script"

du -hs dist/*