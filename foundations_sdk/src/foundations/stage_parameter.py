"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class StageParameter(object):

    def __init__(self, stage):
        self._stage = stage

    def compute_value(self, runtime_data):
        return self._stage.run_same_process(**runtime_data)

    def provenance(self):
        return {'type': 'stage', 'stage_name': self._stage.function_name(), 'stage_uuid': self._stage.uuid()}

    def hash(self, runtime_data):
        from foundations.utils import generate_uuid

        value = self.compute_value(runtime_data)
        return generate_uuid(str(value))

    def enable_caching(self):
        self._stage.enable_caching()

    def __str__(self):
        return 'stage::{}'.format(self._stage.uuid())