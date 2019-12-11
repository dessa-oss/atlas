#!/bin/bash

mkdir atlas_install
cd atlas_install
conda update -n base -c defaults conda --yes
conda create -n atlas_ce_env python=3.6 --yes
source ~/anaconda3/etc/profile.d/conda.sh
conda activate atlas_ce_env
aws s3 cp $1 ./atlas_ce_installer.sh
chmod +x atlas_ce_installer.sh
yes | ./atlas_ce_installer.sh
atlas-server start > /dev/null 2>&1 &
