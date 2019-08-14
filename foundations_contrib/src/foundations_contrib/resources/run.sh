#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
VENV_DIRECTORY=$(mktemp -d)/venv
export PYTHONDONTWRITEBYTECODE=1

cd $BASEDIR && \
  stat run.env> /dev/null 2>&1 && \
  . ./run.env

if [ "${log_level}" = "" ]; then
  log_level=INFO
fi

with_output_redirect () {
  if [ "${log_level}" = "DEBUG" ]; then
    "$@"
  elif [ "${log_level}" = "INFO" ]; then
    "$@" > /dev/null
  elif [ "${log_level}" = "ERROR" ]; then
    "$@" > /dev/null
  else
    "$@" > /dev/null 2> /dev/null
  fi
}

if [[ -z "${python_path}" ]]; then
  python_path=$(which python || which python3)
fi

pip_options="--disable-pip-version-check"

cd $BASEDIR && \
  tar -xf job.tgz && \
  with_output_redirect $python_path -m pip ${pip_options} install virtualenv && \
  with_output_redirect $python_path -m virtualenv --system-site-packages $VENV_DIRECTORY

with_output_redirect stat $VENV_DIRECTORY/bin/activate
if [ $? -eq 0 ]; then
  activate_path=$VENV_DIRECTORY/bin/activate
else
  activate_path=$VENV_DIRECTORY/Scripts/activate
fi

cd $BASEDIR && \
  . $activate_path && \
  with_output_redirect python -m pip install ${pip_options} -r foundations_requirements.txt && \
  with_output_redirect echo Running python version `python --version` located at $(which python) && \
  touch requirements.txt && \
  with_output_redirect python -m pip install ${pip_options} -U -r requirements.txt && \
  PYTHONUNBUFFERED=TRUE python foundations_main.py
  
status=$?

deactivate
rm -rf $VENV_DIRECTORY && \
  rm -rf /tmp/pip* && \
  rm -rf $HOME/.cache/pip

exit $status