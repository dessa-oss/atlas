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
        return self._root()

    def manifest(self):
        import os.path as path

        if not path.exists(self._manifest_path()):
            raise Exception('Manifest file, foundations_package_manifest.yaml not found!')

        with open(self._manifest_path(), 'r') as manifest_file:
            manifest = self._manifest_from_file(manifest_file)

        predict_endpoint_information = manifest['entrypoints']['predict']

        if 'module' not in predict_endpoint_information:
            raise Exception('Prediction module name missing from manifest file!')

        return manifest

    def _root(self):
        return f'/archive/archive/{self._id}/artifacts'

    def _manifest_path(self):
        return f'{self._root()}/foundations_package_manifest.yaml'

    def _manifest_from_file(self, manifest_file):
        import yaml

        try:
            return yaml.load(manifest_file)
        except yaml.parser.ParserError:
            raise Exception('Manifest file was not a valid YAML file!')