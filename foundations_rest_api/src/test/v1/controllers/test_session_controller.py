"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock, patch
import json

# from flask import test_request_context
from foundations_rest_api.global_state import app_manager
from foundations_rest_api.v1.controllers.session_controller import SessionController
from foundations_rest_api.v1.models.session import Session
from werkzeug import ImmutableMultiDict
from flask import request

class TestSessionController(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_session_returns_status_400_if_bad_json(self):
        with app_manager.app().test_request_context(
            data = 'asdafdnas'
        ):
            self.assertEqual(400, SessionController().post().status())

    def test_session_returns_error_message_if_bad_json_different_data(self):
        with app_manager.app().test_request_context(
            data = 'asdafdnasasasas'
        ):
            self.assertEqual('Bad Request', SessionController().post().as_json())
    
    @patch.object(Session, 'auth')
    def test_session_returns_status_200_if_password_valid(self, mock_auth):
        with app_manager.app().test_request_context():
            request.form = ImmutableMultiDict([('password', 'hana')])
            mock_auth.return_value = 200
            self.assertEqual(200, SessionController().post().status())
    
    @patch.object(Session, 'auth')
    def test_session_returns_correct_message_if_status_200_and_password_valid(self, mock_auth):
        with app_manager.app().test_request_context():
            request.form = ImmutableMultiDict([('password', 'lou')])
            mock_auth.return_value = 200
            self.assertEqual('OK', SessionController().post().as_json())

    @patch.object(Session, 'auth')
    def test_session_returns_status_401_if_password_valid(self, mock_auth):
        with app_manager.app().test_request_context():
            request.form = ImmutableMultiDict([('password', 'cat')])
            mock_auth.return_value = 401
            self.assertEqual(401, SessionController().post().status())
    
    @patch.object(Session, 'auth')
    def test_session_returns_correct_message_if_status_401_and_password_valid(self, mock_auth):
        with app_manager.app().test_request_context():
            request.form = ImmutableMultiDict([('password', 'dog')])
            mock_auth.return_value = 401
            self.assertEqual('Unauthorized', SessionController().post().as_json())
       
        