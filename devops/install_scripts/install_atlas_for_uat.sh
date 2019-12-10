#!/bin/bash

mkdir atlas_install
cd atlas_install
conda update -n base -c defaults conda --yes
conda create -n atlas_ce_env python=3.6 --yes
source ~/anaconda3/etc/profile.d/conda.sh
conda activate atlas_ce_env
wget $1
yes | python atlas_ce_installer.py
atlas-server start > /dev/null 2>&1 &
