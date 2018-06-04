#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
PYTHON=python2.7

cd $BASEDIR && \
  tar -xvf job.tgz && \
  $PYTHON -m pip install virtualenv && \
  virtualenv -p $PYTHON venv && \
  . venv/bin/activate && \
  $PYTHON -m pip install -r requirements.txt && \
  $PYTHON main.py
  
status=$?

deactivate
rm -rf venv && \
  rm -rf /tmp/pip* && \
  rm -rf $HOME/.cache/pip

exit $status