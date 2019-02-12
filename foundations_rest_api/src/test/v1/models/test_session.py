"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock, patch

from foundations_rest_api.v1.models.session import Session

class TestSession(unittest.TestCase):
    
    def setUp(self):
        pass
    
    @patch.dict('os.environ', {'FOUNDATIONS_GUI_PASSWORD': 'camel'})
    def test_auth_returns_401_if_incorrect_password(self):
        password ='hippo'
        self.assertEqual(Session.auth(password), 401)
    
    @patch.dict('os.environ',{'FOUNDATIONS_GUI_PASSWORD': 'camel'} )
    def test_auth_returns_200_if_correct_password(self):
        password ='camel'
        self.assertEqual(Session.auth(password), 200)
    
    @patch.dict('os.environ',{'FOUNDATIONS_GUI_PASSWORD': 'rhino'} )
    def test_auth_returns_200_if_correct_password_different_password(self):
        password ='rhino'
        self.assertEqual(Session.auth(password), 200)
