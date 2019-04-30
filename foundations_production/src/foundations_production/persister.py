"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class Persister(object):

    def __init__(self, job_id):
        from foundations_contrib.archiving import get_pipeline_archiver_for_job

        self._job_id = job_id
        self._archiver = get_pipeline_archiver_for_job(job_id)

    def load_user_defined_transformer(self, transformer_id):
        return self._archiver.fetch_artifact('preprocessor/' + transformer_id)

    def save_user_defined_transformer(self, transformer_id, transformer):
        self._archiver.append_artifact(
            'preprocessor/' + transformer_id,
            transformer
        )
