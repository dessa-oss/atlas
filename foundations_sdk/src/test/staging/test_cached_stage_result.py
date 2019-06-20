"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations.staging import cached_stage_result

class TestCachedStageResult(Spec):

    stage = let_mock()
    
    def test_enables_caching_on_the_stage(self):
        cached_stage_result(self.stage)
        self.stage.enable_caching.assert_called_once()
    
    def test_returns_result_of_stage(self):
        result = cached_stage_result(self.stage)
        expected_result = self.stage.run_same_process.return_value
        
        self.assertEqual(expected_result, result)