"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

def _quiet_logs():
    from foundations_contrib.global_state import config_manager
    config_manager['log_level'] = 'FATAL'

_quiet_logs()

from test.test_base_transformer import TestBaseTransformer
from test.test_preprocessor_class import TestPreprocessorClass
from test.test_preprocessor_decorator import TestPreprocessorDecorator
from test.test_transformer import TestTransformer
from test.test_model_class import TestModel
from test.test_production_model import TestProductionModel
from test.test_persister import TestPersister
from test.test_load_model_package import TestLoadModelPackage