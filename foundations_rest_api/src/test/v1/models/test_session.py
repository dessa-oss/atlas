"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock, patch

from foundations_rest_api.v1.models.session import Session

from foundations_internal.testing.helpers import let_patch_mock, set_up
from foundations_internal.testing.helpers.spec import Spec

class TestSession(Spec):
   
    @patch.dict('os.environ', {'FOUNDATIONS_GUI_PASSWORD': 'camel'})
    def test_auth_returns_401_if_incorrect_password(self):
        password ='hippo'
        self.assertFalse(Session.auth(password))
    
    @patch.dict('os.environ',{'FOUNDATIONS_GUI_PASSWORD': 'camel'} )
    def test_auth_returns_200_if_correct_password(self):
        password ='camel'
        self.assertTrue(Session.auth(password))
    
    @patch.dict('os.environ',{'FOUNDATIONS_GUI_PASSWORD': 'rhino'} )
    def test_auth_returns_200_if_correct_password_different_password(self):
        password ='rhino'
        self.assertTrue(Session.auth(password))
