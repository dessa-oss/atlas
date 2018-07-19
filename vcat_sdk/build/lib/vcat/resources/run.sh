#!/usr/bin/env bash

BASEDIR=$(dirname "$0")

cd $BASEDIR && \
  stat run.env> /dev/null 2>&1 && \
  . ./run.env

if [[ -z "${python_path}" ]]; then
  python_path=`which python`
fi

cd $BASEDIR && \
  tar -xf job.tgz && \
  $python_path -m pip install -q virtualenv && \
  $python_path -m virtualenv -q --system-site-packages venv

stat $BASEDIR/venv/bin/activate > /dev/null 2>&1
if [ $? -eq 0 ]; then 
  activate_path=venv/bin/activate
else
  activate_path=venv/Scripts/activate
fi

cd $BASEDIR && \
  . $activate_path && \
  echo Running python version `python --version` located at `which python` && \
  touch requirements.txt && \
  python -m pip install -q -r requirements.txt && \
  python main.py
  
status=$?

deactivate
rm -rf venv && \
  rm -rf /tmp/pip* && \
  rm -rf $HOME/.cache/pip

exit $status