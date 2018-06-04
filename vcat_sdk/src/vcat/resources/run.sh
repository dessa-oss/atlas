#!/usr/bin/env bash

BASEDIR=$(dirname "$0")

cd $BASEDIR && \
  tar -xvf job.tgz && \
  python3 -m pip install virtualenv && \
  virtualenv venv && \
  . venv/bin/activate && \
  python3 -m pip install -r requirements.txt && \
  python3 main.py
  
status=$?

deactivate
rm -rf venv && \
  rm -rf /tmp/pip* && \
  rm -rf $HOME/.cache/pip

exit $status