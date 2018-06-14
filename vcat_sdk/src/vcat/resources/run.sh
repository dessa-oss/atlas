#!/usr/bin/env bash

BASEDIR=$(dirname "$0")

cd $BASEDIR && \
  stat run.env && \
  . ./run.env

if [[ -z "${python_path}" ]]; then
  python_path=`which python`
fi

cd $BASEDIR && \
  tar -xvf job.tgz && \
  $python_path -m pip install virtualenv && \
  virtualenv --system-site-packages venv

stat $BASEDIR/venv/bin/activate
if [ $? -eq 0 ]; then 
  activate_path=venv/bin/activate
else
  activate_path=venv/Scripts/activate
fi

cd $BASEDIR && \
  . $activate_path && \
  $python_path -m pip install -r requirements.txt && \
  $python_path main.py
  
status=$?

deactivate
rm -rf venv && \
  rm -rf /tmp/pip* && \
  rm -rf $HOME/.cache/pip

exit $status