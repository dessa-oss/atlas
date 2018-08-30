#!/usr/bin/env bash

BASEDIR=$(dirname "$0")

cd $BASEDIR && \
  stat run.env> /dev/null 2>&1 && \
  . ./run.env

current_tty=$(tty)

if [ "${log_level}" = "DEBUG" ]; then
  debug_log=$current_tty
  info_log=$current_tty
  error_log=$current_tty
elif [ "${log_level}" = "INFO" ]; then
  debug_log=/dev/null
  info_log=$current_tty
  error_log=$current_tty
elif [ "${log_level}" = "ERROR" ]; then
  debug_log=/dev/null
  info_log=/dev/null
  error_log=$current_tty
else
  debug_log=/dev/null
  info_log=/dev/null
  error_log=/dev/null
fi

if [[ -z "${python_path}" ]]; then
  python_path=$(which python || which python3)
fi

cd $BASEDIR && \
  tar -xf job.tgz && \
  $python_path -m pip install virtualenv 2>$error_log >$debug_log && \
  $python_path -m virtualenv --system-site-packages venv 2>$error_log >$debug_log

stat $BASEDIR/venv/bin/activate >$debug_log 2>$error_log
if [ $? -eq 0 ]; then 
  activate_path=venv/bin/activate
else
  activate_path=venv/Scripts/activate
fi

cd $BASEDIR && \
  . $activate_path && \
  echo Running python version `${python_path} --version` located at ${python_path} >$debug_log && \
  touch requirements.txt && \
  python -m pip install -r requirements.txt >$debug_log 2>$error_log && \
  python main.py
  
status=$?

deactivate
rm -rf venv && \
  rm -rf /tmp/pip* && \
  rm -rf $HOME/.cache/pip

exit $status