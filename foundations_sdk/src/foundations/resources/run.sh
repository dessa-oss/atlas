#!/usr/bin/env bash

BASEDIR=$(dirname "$0")

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
  with_output_redirect $python_path -m virtualenv --system-site-packages venv

with_output_redirect stat $BASEDIR/venv/bin/activate
if [ $? -eq 0 ]; then 
  activate_path=venv/bin/activate
else
  activate_path=venv/Scripts/activate
fi

if [ "${offline_mode}" = "FORCE_ONLINE" ]; then
  echo "Forcing online mode, skipping internet check." >&2
elif [ "${offline_mode}" != "OFFLINE" ]; then
  with_output_redirect echo "Checking for internet connection..."
  with_output_redirect ping -c 3 4.2.2.1

  if [ $? -ne 0 ]; then
    offline_mode=OFFLINE
  fi
fi

if [ "${offline_mode}" = "OFFLINE" ]; then
  echo "No internet connection - using system packages only." >&2
  pip_options="${pip_options} --no-index"
fi

cd $BASEDIR && \
  . $activate_path && \
  with_output_redirect echo Running python version `${python_path} --version` located at ${python_path} && \
  touch requirements.txt && \
  with_output_redirect ${python_path} -m pip install ${pip_options} -r requirements.txt && \
  PYTHONUNBUFFERED=TRUE ${python_path} main.py
  
status=$?

deactivate
rm -rf venv && \
  rm -rf /tmp/pip* && \
  rm -rf $HOME/.cache/pip

exit $status