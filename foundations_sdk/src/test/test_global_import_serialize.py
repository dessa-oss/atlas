"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch
from foundations.serializer import serialize
import dill


class TestGlobalImportSerialization(unittest.TestCase):
    
    @patch.object(dill, 'dumps')
    def test_calls_dumps_with_recurse_true(self, mock_dumps):
        from foundations.serializer import serialize

        item = 'some data to serialize'
        serialize(item)
        mock_dumps.assert_called_with('some data to serialize', protocol=2, recurse=True)
