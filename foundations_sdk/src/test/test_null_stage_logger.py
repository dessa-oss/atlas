"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.null_stage_logger import NullStageLogger

class TestNullStageLogger(unittest.TestCase):
    
    def test_log_metric_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            NullStageLogger().log_metric('loss', 0.56)
    
    def test_pipeline_context_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            NullStageLogger().pipeline_context()
    
    def test_stage_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            NullStageLogger().stage()
    
    def test_stage_context_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            NullStageLogger().stage_context()
    
    def test_stage_config_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            NullStageLogger().stage_config()
