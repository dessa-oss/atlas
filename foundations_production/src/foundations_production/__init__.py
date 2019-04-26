"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

import collections

_model_package = collections.namedtuple('ModelPackage', ['preprocessor', 'model'])

def preprocessor(preprocessor_callback):
    from foundations_production.preprocessor_class import Preprocessor
    return Preprocessor(preprocessor_callback, 'transformer')

def model(preprocessor_callback):
    from foundations_production.preprocessor_class import Preprocessor
    return Preprocessor(preprocessor_callback, 'model')

def load_model_package(job_id):
    from foundations_production.preprocessor_class import Preprocessor
    from foundations_contrib.archiving import get_pipeline_archiver_for_job

    pipeline_archiver = get_pipeline_archiver_for_job(job_id)
    preprocessor_callback = pipeline_archiver.fetch_artifact('preprocessor/transformer.pkl')
    model_callback = pipeline_archiver.fetch_artifact('preprocessor/model.pkl')
    preprocessor = Preprocessor(preprocessor_callback, 'transformer')
    model_preprocessor = Preprocessor(model_callback, 'model')
    return _model_package(preprocessor = preprocessor, model = model_preprocessor)

def _append_module():
    import sys
    from foundations_contrib.global_state import module_manager

    module_manager.append_module(sys.modules[__name__])

_append_module()