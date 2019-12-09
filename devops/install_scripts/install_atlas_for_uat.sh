#!/bin/bash

mkdir atlas_install
cd atlas_install
conda update -n base -c defaults conda --yes
conda create -n atlas_ce_env python=3.6 --yes
source ~/anaconda3/etc/profile.d/conda.sh
conda activate atlas_ce_env
wget https://s3.amazonaws.com/foundations-public/atlas_ce_installer.py
yes | python atlas_ce_installer.py
atlas-server start > /dev/null 2>&1 &
