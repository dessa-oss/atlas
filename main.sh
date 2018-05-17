#!/bin/bash

python -m pip install virtualenv
python -m pip --version
virtualenv venv
. venv/bin/activate
python -m pip --version
python -m pip install -r requirements.txt && python main.py
deactivate
