"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_rest_api.app_manager import AppManager 


class TestAppManager(unittest.TestCase):
    def test_app_initialize(self):
        from flask import Flask

        app_manager = AppManager()
        app_manager.app()
        self.assertTrue(isinstance(app_manager.app(), Flask))
    
    def test_always_returns_same_app(self):
        app_manager = AppManager()
        initial_app = app_manager.app()
        second_app = app_manager.app()
        self.assertEqual(initial_app, second_app)

