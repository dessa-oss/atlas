#!/bin/sh

cwd=`pwd`

. ./devops/load_nexus_credentials.sh

export LOCAL_DOCKER_SCHEDULER_HOST=localhost
export FOUNDATIONS_SCHEDULER_HOST=localhost
export REDIS_HOST=localhost
export REDIS_PORT=6379 
export REMOTE_FOUNDATIONS_HOME="$cwd/testing/orbit_acceptance/fixtures/end-to-end-acceptance/foundations_home"


pip install -r requirements_test.txt \
    && ./devops/build_scripts/build_all_dist.sh \
    && ./run_unit_tests.sh \
    && ./run_coverage_tests.sh \
    && ./run_integration_tests.sh \
    && cd $cwd/testing \
        && python -Wi -m unittest -f -v acceptance \
        && python -Wi -m unittest -f -v stageless_acceptance \
        && python -Wi -m unittest -f -v orbit_acceptance \
    && cd $cwd/foundations_rest_api/src \
        && python -Wi -m unittest -f -v acceptance \
    && cd $cwd/foundations_ui \
        && yarn install \
        && yarn run test \
        && node_modules/.bin/eslint . \
    && cd $cwd/foundations_ui_orbit \
        && yarn install \
        && yarn run test \
        && node_modules/.bin/eslint . \
    && cd $cwd \
        tar -czvf coverage.tar.gz coverage_results \
    echo "Successfully ran all test"

