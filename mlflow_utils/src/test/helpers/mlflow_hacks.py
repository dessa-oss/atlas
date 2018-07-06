"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class ArtifactInfo(object):

    def __init__(self):
        self.artifact = None
        self.artifact_name = None

ARTIFACT_INFO = ArtifactInfo()

def log_artifact(file_path, name):
    with open(file_path, 'rb') as file:
        ARTIFACT_INFO.artifact = file.read()
    ARTIFACT_INFO.artifact_name = name


def get_artifact_info():
    return ARTIFACT_INFO.artifact, ARTIFACT_INFO.artifact_name
