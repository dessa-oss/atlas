#!/bin/bash

# . /archive/archive/$JOB_ID/artifacts/venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/python3.6/dist-packages/foundations:/usr/local/lib/python3.6/dist-packages/foundations_contrib" && \
python -m foundations_model_package
