"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

def user_token():
    from foundations_contrib.utils import foundations_home
    from os.path import expanduser, join
    import yaml
    import os

    token = os.getenv('FOUNDATIONS_TOKEN', None)

    if not token:
        credential_filepath = expanduser(join(foundations_home(), "credentials.yaml"))
        if not os.path.isfile(credential_filepath):
            return None
        with open(credential_filepath, "r") as file:
            credential_dict = yaml.load(file)
        if "default" not in credential_dict:
            return None
        if "token" not in credential_dict["default"]:
            return None
        token = credential_dict["default"]["token"]

    return token