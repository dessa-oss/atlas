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

from foundations_internal.testing.helpers import let, let_patch_mock, set_up
from foundations_internal.testing.helpers.spec import Spec

class TestSessionController(Spec):

    @let
    def session_controller(self):
        return SessionController()

    mock_auth = let_patch_mock('foundations_rest_api.v1.models.session.Session.auth')

    @set_up
    def set_up(self):
        self._ensure_mock_auth_used()

    def _ensure_mock_auth_used(self):
        self.mock_auth

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
    
    def test_session_returns_correct_message_if_status_200_and_password_valid(self):
        self.session_controller.params = {'password': 'cave'}
        self.mock_auth.return_value = True 
        self.assertEqual('OK', self.session_controller.post().as_json())

    def test_session_returns_status_401_if_password_valid(self):
        self.session_controller.params = {'password': 'cave'}
        self.mock_auth.return_value = False
        self.assertEqual(401, self.session_controller.post().status())
    
    def test_session_returns_correct_message_if_status_401_and_password_valid(self):
        self.session_controller.params = {'password': 'cave'}
        self.mock_auth.return_value = False
        self.assertEqual('Unauthorized', self.session_controller.post().as_json())