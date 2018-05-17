#!/bin/bash

python -m pip install virtualenv && \
  virtualenv venv && \
  . venv/bin/activate && \
  python -m pip install -r requirements.txt && \
  python main.py && \
  deactivate
