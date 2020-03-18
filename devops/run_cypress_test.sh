#!/bin/bash

cwd=`pwd`
F9S_ENV_TYPE=$1

echo "checking if redis-cli is installed and available ....."
redis-cli --version >/dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "redis-cli is not available. The cli tool is required to clear redis between tests"
  exit 1
fi

UI_FOLDER="foundations_ui"
FIXTURE_FOLDER="atlas_scheduler"

cd $UI_FOLDER \
    && yarn install --silent \
    && npm run cy:run -- --headed