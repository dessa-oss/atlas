"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def load_parameters():
    try:
        return _read_from_parameters_file()
    except FileNotFoundError:
        return {}

def _read_from_parameters_file():
    import json

    with open('foundations_job_parameters.json', 'r') as parameters_file:
        return json.load(parameters_file)