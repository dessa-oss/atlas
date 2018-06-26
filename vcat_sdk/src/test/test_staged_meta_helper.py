"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from vcat.staged_meta_helper import StagedMetaHelper


class TestStagedMetaHelper(unittest.TestCase):

    def test_inner_module_returns_none_when_no_module(self):
        result = StagedMetaHelper('potato').inner_module()
        self.assertEqual(None, result)

    def test_inner_module_returns_unstaged_module(self):
        import pandas
        result = StagedMetaHelper('staged_pandas').inner_module()
        self.assertEqual(pandas, result)
