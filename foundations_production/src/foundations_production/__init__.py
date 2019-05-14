"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

import collections
from foundations_production.transformer import Transformer
from foundations_production.model_class import Model
from foundations_production.model_package import ModelPackage

def preprocessor(preprocessor_callback):
    from foundations_production.preprocessor_class import Preprocessor
    return Preprocessor(preprocessor_callback, 'transformer')

def load_model_package(job_id):
    from foundations_contrib.archiving import get_pipeline_archiver_for_job
    from foundations_production.production_model import ProductionModel
    from foundations_production.preprocessor_class import Preprocessor
    from foundations_contrib.global_state import redis_connection
    from foundations_contrib.job_data_redis import JobDataRedis

    if not JobDataRedis.is_job_completed(job_id, redis_connection):
        raise KeyError('Model Package ID {} does not exist'.format(job_id))

    pipeline_archiver = get_pipeline_archiver_for_job(job_id)
    preprocessor = Preprocessor.load_preprocessor(pipeline_archiver, 'transformer', job_id)
    model = ProductionModel(job_id)
    return ModelPackage(preprocessor=preprocessor, model=model)

def _append_module():
    import sys
    from foundations_contrib.global_state import module_manager

    module_manager.append_module(sys.modules[__name__])

_append_module()