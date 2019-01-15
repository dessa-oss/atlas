"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
import mock
from pathlib import Path

from scaffold import Scaffold

class TestScaffold(unittest.TestCase):
	def test_intial_test(self):
		scaffold = Scaffold()
		expected_path = Path('/Users/pippinlee/github/foundations/foundations_sdk/foundations_init/template')
		template_path = scaffold.template_path()
		self.assertEqual(expected_path, template_path)