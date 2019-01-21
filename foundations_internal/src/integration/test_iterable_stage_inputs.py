"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock
from foundations import create_stage

class TestIterableStageInputs(unittest.TestCase):
    
    def test_list_of_stages(self):
        stage = create_stage(self._callback)(5)
        stage2 = create_stage(self._callback)(512)
        stage3 = create_stage(self._callback)([stage, stage2, 6])
        self.assertEqual([5, 512, 6], stage3.run_same_process())
    
    def test_list_of_stages_recursive(self):
        stage = create_stage(self._callback)(5)
        stage2 = create_stage(self._callback)([stage])
        stage3 = create_stage(self._callback)([[stage, stage2], 6])
        self.assertEqual([[5, [5]], 6], stage3.run_same_process())
    
    def test_dict_of_stages(self):
        stage = create_stage(self._callback)(5)
        stage2 = create_stage(self._callback)(512)
        stage3 = create_stage(self._callback)({'hello': stage, 'world': stage2, 'potato': 6})
        self.assertEqual({'hello': 5, 'potato': 6, 'world': 512}, stage3.run_same_process())
    
    def test_dict_of_stages_recursive(self):
        stage = create_stage(self._callback)(5)
        stage2 = create_stage(self._callback)({'hello': stage})
        stage3 = create_stage(self._callback)({'hello': {'hello': stage, 'world': stage2}, 'goodbye': 6})
        self.assertEqual({'goodbye': 6, 'hello': {'hello': 5, 'world': {'hello': 5}}}, stage3.run_same_process())
    
    def test_mix_of_stages_recursive(self):
        stage = create_stage(self._callback)(5)
        stage2 = create_stage(self._callback)({'hello': stage})
        stage3 = create_stage(self._callback)({'hello': [stage, stage2], 'goodbye': 6})
        self.assertEqual({'goodbye': 6, 'hello': [5, {'hello': 5}]}, stage3.run_same_process())

    def _callback(self, input):
        return input