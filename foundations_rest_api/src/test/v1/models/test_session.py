"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock, patch

from foundations_rest_api.v1.models.session import Session

from foundations_internal.testing.helpers import let, let_patch_mock, set_up
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
    
    @let
    def fake_token(self):
        import faker
        return faker.Faker().sha1()

    @let
    def session(self):
        return Session(token=self.fake_token)

    mock_redis = let_patch_mock('foundations.global_state.redis_connection')

    @set_up
    def set_up(self):
        self.mock_redis
    
    def test_session_has_token(self):
        self.assertEquals(self.session.token, self.fake_token)
    
    def test_save_saved_to_redis(self):
        self.session.save()
        self.mock_redis.set.assert_called_with('session:{}'.format(self.fake_token), 'valid')


