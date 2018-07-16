"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class ArgumentHasher(object):

    def __init__(self, args, kwargs):
        self._args = args
        self._kwargs = kwargs

    def make_hash(self):
        from vcat.utils import merged_uuids

        return merged_uuids(self._arg_hashes() + self._kwarg_hashes())

    def _arg_hashes(self):
        return [self._make_argument_hash(None, arg) for arg in self._args]

    def _kwarg_hashes(self):
        from vcat.utils import generate_uuid

        results = []
        for key, value in self._kwargs.items():
            results.append(generate_uuid(key))
            results.append(self._make_argument_hash(key, value))
        return results

    def _make_argument_hash(self, key, item):
        from vcat.utils import make_uuid
        from vcat.utils import generate_uuid
        from vcat.pipeline import Pipeline
        from vcat.stage_connector_wrapper import StageConnectorWrapper
        from vcat.hyperparameter import Hyperparameter

        if isinstance(item, Pipeline) or isinstance(item, StageConnectorWrapper) or isinstance(item, Pipeline):
            return item.uuid()

        if isinstance(item, Hyperparameter):
            return generate_uuid(item.name or key)

        return make_uuid(item, self._make_argument_hash)
