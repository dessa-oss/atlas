#!/bin/bash

source dev_env.sh
export REDIS_URL=redis://localhost:6379
export FOUNDATIONS_SCHEDULER_URL=localhost:5000

export REDIS_HOST=redis
export ARCHIVE_DIR=~/.foundations/job_data
export WORKING_DIR=~/.foundations/local_docker_scheduler/work_dir
export NUM_WORKERS=0

export REACT_APP_API_URL=http://127.0.0.1:37222/api/v1/
export REACT_APP_ATLAS_URL=http://127.0.0.1:37722/api/v2beta/
export REACT_APP_APIARY_URL=http://private-d03986-iannelladessa.apiary-mock.com/api/v1/

python devops/startup_atlas_api.py && \
  python devops/startup_orbit_api.py && \
  cd ../local_docker_scheduler && python -m local_docker_scheduler -p 5000 > /var/foundations/scheduler.log 2>&1 &

if $? == 0; then
  cd foundations_ui_orbit && \
    yarn install && \
    yarn start
fi