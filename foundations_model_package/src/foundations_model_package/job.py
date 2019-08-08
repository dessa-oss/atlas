"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class Job(object):
    
    def __init__(self, job_id):
        self._id = job_id
        self._manifest = None

    def id(self):
        return self._id

    def root(self):
        return self._root()

    def manifest(self):
        if self._manifest is None:
            self._load_manifest()

        return self._manifest

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

    def _load_manifest(self):
        import os.path as path
        from foundations_model_package.manifest_validator import ManifestValidator

        if not path.exists(self._manifest_path()):
            raise Exception('Manifest file, foundations_package_manifest.yaml not found!')

        with open(self._manifest_path(), 'r') as manifest_file:
            model_package_manifest = self._manifest_from_file(manifest_file)

        ManifestValidator(model_package_manifest).validate_manifest()

        self._manifest = model_package_manifest