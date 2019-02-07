"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock, patch

# from flask import test_request_context
from foundations_rest_api.global_state import app_manager
from foundations_rest_api.v1.controllers.session_controller import SessionController

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
            self.assertEqual('Bad request', SessionController().post().as_json())
    
