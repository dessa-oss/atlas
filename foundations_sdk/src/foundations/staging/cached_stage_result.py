"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def cached_stage_result(stage):
    stage.enable_caching()
    return stage.run_same_process()

def foundations_stage(function, *args, **kwargs):
    from foundations.global_state import foundations_context
    return foundations_context.pipeline().stage(function, *args, **kwargs)

