"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class Job(object):
    
    def __init__(self, job_id):
        self._id = job_id

    def id(self):
        return self._id

    def root(self):
        return f'/archive/archive/{self._id}/artifacts'

    def manifest(self):
        import yaml

        with open(f'/archive/archive/{self._id}/artifacts/foundations_package_manifest.yaml', 'r') as manifest_file:
            manifest = yaml.load(manifest_file)

        return manifest