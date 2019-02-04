"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch
from foundations_internal.serializer import serialize
import dill


class TestGlobalImportSerialization(unittest.TestCase):

    @patch.object(dill, 'dumps')
    def test_calls_dumps_with_recurse_true(self, mock_dumps):
        item = 'some data to serialize'
        serialize(item)
        mock_dumps.assert_called_with(
            'some data to serialize', protocol=2, recurse=True)

    @patch.object(dill, 'dumps')
    def test_calls_dumps_with_recurse_true_with_different_data(self, mock_dumps):
        item = 'lou data'
        serialize(item)
        mock_dumps.assert_called_with('lou data', protocol=2, recurse=True)
