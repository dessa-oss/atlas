"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch

from foundations_core_rest_api_components.app_manager import AppManager


class TestAppManager(unittest.TestCase):
    def test_app_initialize(self):
        from flask import Flask

        app_manager = AppManager()
        self.assertTrue(isinstance(app_manager.app(), Flask))

    def test_always_returns_same_app(self):
        app_manager = AppManager()
        initial_app = app_manager.app()
        second_app = app_manager.app()
        self.assertEqual(initial_app, second_app)
    
    @patch('flask_cors.CORS')
    def test_uses_cors(self, mock):
        app_manager = AppManager()
        app = app_manager.app()
        mock.assert_called_with(app, supports_credentials=True)

    @patch('flask_cors.CORS')
    def test_uses_calls_cors_only_once(self, mock):
        app_manager = AppManager()
        app_manager.app()
        app_manager.app()
        mock.assert_called_once()

    def test_api_initialize(self):
        from flask_restful import Api

        app_manager = AppManager()
        self.assertTrue(isinstance(app_manager.api(), Api))

    def test_always_returns_same_api(self):
        app_manager = AppManager()
        initial_api = app_manager.api()
        second_api = app_manager.api()
        self.assertEqual(initial_api, second_api)

    def test_that_api_uses_proper_app(self):
        app_manager = AppManager()
        api = app_manager.api()
        self.assertEqual(api.app, app_manager.app())
