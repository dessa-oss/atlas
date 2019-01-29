"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_internal.config.config_translator import ConfigTranslator

class TestConfigTranslator(unittest.TestCase):

    def setUp(self):
        self._translator = ConfigTranslator()
    
    def test_raises_error_when_no_translator_defined(self):
        with self.assertRaises(ValueError) as error_context:
            self._translator.translate({'job_deployment_env': 'gcp'})

        self.assertIn('Got invalid deployment environment `gcp`', error_context.exception.args)        
    
    def test_raises_error_when_no_translator_defined_different_name(self):
        with self.assertRaises(ValueError) as error_context:
            self._translator.translate({'job_deployment_env': 'azure'})

        self.assertIn('Got invalid deployment environment `azure`', error_context.exception.args)        
