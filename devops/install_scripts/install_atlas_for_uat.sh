#!/bin/bash

mkdir atlas_install && \
cd atlas_install && \
conda create -n atlas_ce_env python=3.6 --yes && \
source ~/anaconda3/etc/profile.d/conda.sh && \
conda activate atlas_ce_env && \
aws s3 cp --quiet $1 ./atlas_ce_installer.sh && \
echo 'Downloaded successfully' && \
chmod +x atlas_ce_installer.sh && \
yes | ./atlas_ce_installer.sh
atlas-server start > /dev/null 2>&1 &
mkdir -p test && \
echo import foundations >> test/main.py && \
chmod +x /home/ubuntu/wait_for_successful_job_submission.sh && \
bash /home/ubuntu/wait_for_successful_job_submission.sh 50