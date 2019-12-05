#!/bin/bash

pip install ansible==2.8.2 boto==2.49.0 boto3==1.9.86 botocore==1.12.183 wget==3.2
pip install -i https://$NEXUS_USER:$NEXUS_PASSWORD@$NEXUS_PYPI_PATH --extra-index-url https://pypi.org/simple -U -r requirements_test.txt
