"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from mock import Mock, patch

from foundations_core_rest_api_components.v1.models.session import Session

from foundations_spec.helpers import let, let_patch_mock, set_up
from foundations_spec.helpers.spec import Spec

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
    def random_token_data(self):
        import base64
        return base64.b64decode(self.fake_token)

    @let
    def session(self):
        return Session(token=self.fake_token)

    @let
    def session_key(self):
        return 'session:{}'.format(self.fake_token)

    mock_redis = let_patch_mock('foundations_contrib.global_state.redis_connection')
    mock_token_generator = let_patch_mock('Crypto.Random._UserFriendlyRNG.RNGFile.read')

    @set_up
    def set_up(self):
        self.mock_token_generator.return_value = self.random_token_data

    def test_session_has_token(self):
        self.assertEquals(self.session.token, self.fake_token)
    
    def test_save_saved_to_redis(self):
        self.session.save()
        self.mock_redis.set.assert_called_with(self.session_key, 'valid')

    def test_save_returns_itself(self):
        result = self.session.save()
        self.assertTrue(result is self.session)
    
    def test_save_sets_expiry_in_redis(self):
        self.session.save()
        self.mock_redis.expire.assert_called_with(self.session_key, 2592000)

    def test_find_returns_empty_lazy_result(self):
        self.mock_redis.get.return_value = None
        self.assertIsNone(Session.find(token=self.fake_token).evaluate())
    
    def test_find_gets_token_in_redis(self):
        result = Session.find(token=self.fake_token).evaluate()
        self.assertEqual(self.session, result)
    
    def test_find_gets_with_correct_parameters(self):
        Session.find(token=self.fake_token).evaluate()
        self.mock_redis.get.assert_called_with(self.session_key)

    def test_create_generates_token(self):
        self.mock_token_generator.return_value = self.random_token_data
        session = Session.create()
        self.assertEquals(self.fake_token, session.token)
    
    def test_create_returns_session_with_token(self):
        self.mock_token_generator.return_value = self.random_token_data
        session = Session.create()
        self.assertEquals(session, Session(token=self.fake_token))

    @patch('foundations_core_rest_api_components.v1.models.session.Session.save')
    def test_create_saves_session(self, mock_save):
        session = Session.create()
        mock_save.assert_called()

    def test_is_authorized_returns_true_with_no_password(self):
        self.assertTrue(Session.is_authorized({}))
    
    @patch.dict('os.environ',{'FOUNDATIONS_GUI_PASSWORD': 'platypus'} )
    def test_authorized_returns_false_with_password_no_cookies(self):
        self.assertFalse(Session.is_authorized({}))
    
    @patch.dict('os.environ',{'FOUNDATIONS_GUI_PASSWORD': 'platypus'} )
    def test_authorized_returns_false_with_password_no_token_cookie(self):
        self.assertFalse(Session.is_authorized({'peanut': 'butter'}))

    @patch.dict('os.environ',{'FOUNDATIONS_GUI_PASSWORD': 'platypus'} )
    def test_authorized_returns_false_with_password_and_valid_cookie(self):
        self.assertTrue(Session.is_authorized({'auth_token': 'stuff'}))

    @patch.dict('os.environ',{'FOUNDATIONS_GUI_PASSWORD': 'platypus'} )
    def test_authorized_returns_false_with_password_and_invalid_cookie(self):
        self.mock_redis.get.return_value = None
        self.assertFalse(Session.is_authorized({'auth_token': 'stuff'}))

    @patch.dict('os.environ',{'FOUNDATIONS_GUI_PASSWORD': 'platypus'} )
    def test_authorized_uses_correct_token(self):
        Session.is_authorized({'auth_token': self.fake_token})
        self.mock_redis.get.assert_called_with(self.session_key)