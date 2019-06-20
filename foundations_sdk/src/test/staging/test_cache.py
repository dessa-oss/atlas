"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations.staging import cache

class TestCache(Spec):
    
    mock_cached_stage_result = let_patch_mock('foundations.staging.cached_stage_result.cached_stage_result')
    mock_foundations_stage = let_patch_mock('foundations.staging.cached_stage_result.foundations_stage')

    mock_foundations_stage = let_mock()

    @set_up
    def set_up(self):
        pass
