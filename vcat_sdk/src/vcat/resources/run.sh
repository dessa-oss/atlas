#!/usr/bin/env bash

BASEDIR=$(dirname "$0")

cd $BASEDIR && \
  python -m pip install virtualenv && \
  virtualenv venv && \
  . venv/bin/activate && \
  python -m pip install -r requirements.txt && \
  python main.py
  
status=$?

deactivate
rm -rf venv && \
  rm -rf /tmp/pip* && \
  rm -rf $HOME/.cache/pip

exit $status