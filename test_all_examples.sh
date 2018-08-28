#!/bin/bash

rm -rf /tmp/archives

python -m virtualenv --system-site-packages /tmp/examples-venv
source /tmp/examples-venv/bin/activate
python -m pip install -r requirements.txt

bash build_dist.sh

cd examples

# make sure to add a space after module name
modules=""
modules+="cache "
modules+="grid_search "
modules+="impute_data "
modules+="loading_data "
modules+="local_cache "
modules+="logistic_regression "
modules+="one_hot_encode "
modules+="replacing_nulls "
modules+="fetch_job_information "
modules+="fetch_results "

for module in ${modules}
do
    python -Wi -m ${module}

    if [ $? -ne 0 ]
    then
        break
    fi
done

deactivate
rm -rf /tmp/examples-venv
rm -rf /tmp/foundations_example*