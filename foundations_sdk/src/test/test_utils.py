"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

import unittest
from mock import patch

import foundations.utils as utils

class TestUtils(unittest.TestCase):
    def test_whoami_user_pl(self):
        env = {"USER": "pl"}
        with patch("os.environ", env):
            self.assertEqual(utils.whoami(), "pl")

    def test_whoami_user_kb(self):
        env = {"USER": "kb"}
        with patch("os.environ", env):
            self.assertEqual(utils.whoami(), "kb")

    def test_whoami_uses_logname_if_user_not_set(self):
        env = {"LOGNAME": "kb"}
        with patch("os.environ", env):
            self.assertEqual(utils.whoami(), "kb")

    def test_whoami_uses_logname_if_user_not_set_different_logname(self):
        env = {"LOGNAME": "pl"}
        with patch("os.environ", env):
            self.assertEqual(utils.whoami(), "pl")