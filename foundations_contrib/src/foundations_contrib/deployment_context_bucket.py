"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class DeploymentContextBucket(object):
    
    def __init__(self, local_bucket, deploy_bucket):
        self._local_bucket = local_bucket
        self._deploy_bucket = deploy_bucket

    def upload_from_string(self, name, data):
        return self._get_bucket().upload_from_string(name, data)

    def upload_from_file(self, name, input_file):
        return self._get_bucket().upload_from_file(name, input_file)

    def exists(self, name):
        return self._get_bucket().exists(name)

    def download_as_string(self, name):
        return self._get_bucket().download_as_string(name)

    def download_to_file(self, name, output_file):
        return self._get_bucket().download_to_file(name, output_file)

    def list_files(self, pathname):
        return self._get_bucket().list_files(pathname)

    def remove(self, name):
        return self._get_bucket().remove(name)

    def move(self, source, destination):
        return self._get_bucket().move(source, destination)
    
    def _get_bucket(self):
        if self._is_deployment():
            return self._deploy_bucket
        else:
            return self._local_bucket

    def _is_deployment(self):
        from foundations.global_state import config_manager
        return config_manager.config().get('_is_deployment', False)