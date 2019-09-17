#! /bin/sh

cd /job/job_source
if [ -f requirements.txt ]; then
    echo "Installing user requirements"
    pip install -r requirements.txt
else
    echo "No user requirements found."
fi
python "$@"
