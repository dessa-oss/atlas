"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def _install():
    from vcat.global_state import middleware_manager
    from vcat_mlflow.stage_log_middleware import StageLogMiddleware
    from vcat_mlflow.parameter_middleware import ParameterMiddleware

    middleware_manager.append_stage('MLFlowStageLog', StageLogMiddleware)
    middleware_manager.add_stage_middleware_before(
        'ArugmentFiller', 'MLFlowParameter', ParameterMiddleware)
