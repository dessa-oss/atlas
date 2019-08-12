"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock, patch
import json

from foundations_rest_api.global_state import app_manager
from foundations_rest_api.v1.controllers.session_controller import SessionController

from foundations_spec.helpers import let, let_patch_mock, set_up
from foundations_spec.helpers.spec import Spec

class TestSessionController(Spec):

    @let
    def session_controller(self):
        return SessionController()
    
    @let
    def random_token(self):
        from faker import Faker
        return Faker().sha256()

    @let
    def random_cookie(self):
        return {'auth_token': self.random_token}

    mock_auth = let_patch_mock('foundations_rest_api.v1.models.session.Session.auth')
    mock_create = let_patch_mock('foundations_rest_api.v1.models.session.Session.create')

    def test_session_returns_status_400_if_bad_json(self):
        self.session_controller.params = {'hats': 'cold'}
        self.assertEqual(400, self.session_controller.post().status())

    def test_session_returns_error_message_if_bad_json_different_data(self):
        self.session_controller.params = {'bats': 'cave'}
        self.assertEqual(400, self.session_controller.post().status())
    
    def test_session_calls_session_auth_when_password_exists(self):
        self.session_controller.params = {'password': 'cave'}
        self.session_controller.post()
        self.mock_auth.assert_called_with('cave')
    
    def test_session_calls_session_auth_when_password_exists_different_password(self):
        self.session_controller.params = {'password': 'dave'}
        self.session_controller.post()
        self.mock_auth.assert_called_with('dave')
    
    def test_session_returns_status_200_if_password_valid(self):
        self.session_controller.params = {'password': 'cave'}
        self.mock_auth.return_value = True
        self.assertEqual(200, self.session_controller.post().status())
    
    def test_session_returns_correct_message_if_password_valid(self):
        self.session_controller.params = {'password': 'cave'}
        self.mock_auth.return_value = True 
        self.assertEqual('OK', self.session_controller.post().as_json())

    def test_session_calls_session_save_if_password_valid(self):
        self.session_controller.params = {'password': 'cave'}
        self.mock_auth.return_value = True 
        self.session_controller.post()
        self.mock_create.assert_called()

    @patch('foundations_core_rest_api_components.response.Response.constant')
    def test_session_calls_response_with_token_if_password_valid(self, mock_constant_response):

        mock_session_instance = Mock()
        mock_session_instance.token = self.random_token

        self.session_controller.params = {'password': 'cave'}
        self.mock_auth.return_value = True 
        self.mock_create.return_value = mock_session_instance
        self.session_controller.post()
        mock_constant_response.assert_called_with('OK', status=200, cookie=self.random_cookie)
    
    def test_session_calls_response_without_token_if_password_invalid(self):
        self.session_controller.params = {'password': 'cave'}
        self.mock_auth.return_value = False 
        self.assertIsNone(self.session_controller.post().cookie())

    def test_session_returns_status_401_if_password_valid(self):
        self.session_controller.params = {'password': 'cave'}
        self.mock_auth.return_value = False
        self.assertEqual(401, self.session_controller.post().status())
    
    def test_session_returns_correct_message_if_status_401_and_password_valid(self):
        self.session_controller.params = {'password': 'cave'}
        self.mock_auth.return_value = False
        self.assertEqual('Unauthorized', self.session_controller.post().as_json())