"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch
from foundations_rest_api.utils.api_resource import api_resource


class TestAPIResource(unittest.TestCase):
    class Mock(object):
        pass

    def test_returns_class(self):
        klass = api_resource('path/to/resource')(self.Mock)
        self.assertEqual(klass, self.Mock)