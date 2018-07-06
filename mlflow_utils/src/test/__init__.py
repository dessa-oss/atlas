"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def _hack_mlflow():
    import mlflow
    from sys import modules
    import test.helpers.mlflow_hacks

    modules['mlflow'] = test.helpers.mlflow_hacks

_hack_mlflow()

from test.test_stage_output_middleware import TestStageOutputMiddleware