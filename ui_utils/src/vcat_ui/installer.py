"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def _install():
    from vcat.global_state import middleware_manager
    from vcat_ui.stage_log_middleware import StageLogMiddleware
    from vcat_ui.parameter_middleware import ParameterMiddleware
    from vcat_ui.stage_output_middleware import StageOutputMiddleware

    middleware_manager.append_stage('MLFlowStageLog', StageLogMiddleware)
    middleware_manager.add_stage_middleware_before(
        'ArugmentFiller', 'MLFlowParameter', ParameterMiddleware)
    middleware_manager.add_stage_middleware_before(
        'StageOutput', 'MLFlowStageOutputMiddleware', StageOutputMiddleware)
