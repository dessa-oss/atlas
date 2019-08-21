"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Katherine Bancroft <k.bancroft@dessa.com>, 11 2018
"""

from foundations_spec import *
from foundations_contrib.utils import foundations_home

class TestFoundationsHome(Spec):

    @let
    def override_home(self):
        return self.faker.uri_path()
    
    def test_foundations_home_returns_default_home(self):
        self.assertEqual('~/.foundations', foundations_home())

    def test_foundations_home_returns_environment_home_when_specified(self):
        override_environment = {'FOUNDATIONS_HOME': self.override_home}
        self.patch('os.environ', override_environment)

        self.assertEqual(self.override_home, foundations_home())