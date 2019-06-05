#!/bin/bash

pip install -i https://$NEXUS_USER:$NEXUS_PASSWORD@$NEXUS_PYPI_PATH --extra-index-url https://pypi.org/simple -U -r test_requirements.txt