"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class Transformer(object):
    
    def __init__(self, user_transformer_class, *args, **kwargs):
        from foundations_production.base_transformer import BaseTransformer
        from foundations_production.preprocessor_class import Preprocessor
        from foundations_production.persister import Persister
        import foundations

        self._columns = kwargs.pop('list_of_columns', None)
        user_stage = foundations.create_stage(user_transformer_class)(*args, **kwargs)
        self._base_transformer = BaseTransformer(Preprocessor.active_preprocessor, Persister(self._get_pipeline_archiver()), user_stage)

    def fit(self, data):
        self._base_transformer.fit(self._column_data(data))

    def transform(self, data):
        return self._base_transformer.transformed_data(self._column_data(data))

    def _column_data(self, data):
        if self._columns is not None:
            return data[self._columns]
        else:
            return data
    
    @staticmethod
    def _get_pipeline_archiver():
        from foundations_internal.pipeline_archiver import PipelineArchiver
        from foundations_contrib.archiving import load_archive
        from foundations_contrib.global_state import foundations_context

        job_id = foundations_context.job_id()
        artifact_archive = load_archive('artifact_archive')

        return PipelineArchiver(job_id, None, None, None, None, None, artifact_archive, None)