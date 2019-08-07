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
            model_package_manifest = self._manifest_from_file(manifest_file)

        _ManifestValidator(model_package_manifest).validate_manifest()

        return model_package_manifest

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

class _ManifestValidator(object):

    def __init__(self, model_package_manifest):
        self._model_package_manifest = model_package_manifest

    def validate_manifest(self):
        self._check_entrypoints_section_is_in_manifest()
        self._validate_predict_entrypoint()

    def _validate_predict_entrypoint(self):
        self._check_entrypoint_is_in_manifest('predict')

        for required_entrypoint_information in ['module', 'function']:
            self._check_entrypoint_information_is_in_manifest(required_entrypoint_information, 'predict')

    def _check_entrypoints_section_is_in_manifest(self):
        if 'entrypoints' not in self._model_package_manifest:
            raise Exception('Entrypoints section missing from manifest file!')

    def _check_entrypoint_is_in_manifest(self, entrypoint):
        if entrypoint not in self._model_package_manifest['entrypoints']:
            raise Exception('Prediction entrypoint missing from manifest file!')

    def _check_entrypoint_information_is_in_manifest(self, required_entry, entrypoint):
        predict_endpoint_information = self._model_package_manifest['entrypoints'][entrypoint]

        if required_entry not in predict_endpoint_information:
            raise Exception(f'Prediction {required_entry} name missing from manifest file!')