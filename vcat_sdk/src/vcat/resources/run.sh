#!/usr/bin/env bash

BASEDIR=$(dirname "$0")

cd $BASEDIR && \
  tar -xvf job.tgz && \
  python -m pip install virtualenv && \
  virtualenv --system-site-packages venv

stat $BASEDIR/venv/bin/activate
if [ $? -eq 0 ]; then 
  activate_path=venv/bin/activate
else
  activate_path=venv/Scripts/activate
fi

cd $BASEDIR && \
  . $activate_path && \
  python -m pip install -r requirements.txt && \
  python main.py
  
status=$?

deactivate
rm -rf venv && \
  rm -rf /tmp/pip* && \
  rm -rf $HOME/.cache/pip

exit $status