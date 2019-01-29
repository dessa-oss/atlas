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
    
    def test_raises_error_when_no_environment_provided(self):
        with self.assertRaises(ValueError) as error_context:
            self._translator.translate({})

        self.assertIn('Got invalid deployment environment `None`', error_context.exception.args)        
    
    def test_calls_translate_with_existing_environment(self):
        azure = Mock()
        azure.translate.return_value = 'some configured azure environment'
        self._translator.add_translator('azure', azure)

        translation = self._translator.translate({'job_deployment_env': 'azure'})
        self.assertEqual('some configured azure environment', translation)
    
    def test_calls_translate_with_existing_environment_different_environment(self):
        gcp = Mock()
        gcp.translate.return_value = 'gcp environment with configured data'
        self._translator.add_translator('gcp', gcp)

        translation = self._translator.translate({'job_deployment_env': 'gcp'})
        self.assertEqual('gcp environment with configured data', translation)
    
    def test_calls_translate_with_correct_params(self):
        azure = Mock()
        self._translator.add_translator('azure', azure)

        self._translator.translate({'job_deployment_env': 'azure'})
        azure.translate.assert_called_with({'job_deployment_env': 'azure'})
    
    def test_calls_translate_with_correct_params_different_params(self):
        azure = Mock()
        self._translator.add_translator('azure', azure)

        self._translator.translate({'job_deployment_env': 'azure', 'ip_address': '11.22.33.44'})
        azure.translate.assert_called_with({'job_deployment_env': 'azure', 'ip_address': '11.22.33.44'})
    
    def test_calls_translate_with_multiple_environments(self):
        gcp = Mock()
        gcp.translate.return_value = 'gcp environment with configured data'
        self._translator.add_translator('gcp', gcp)

        azure = Mock()
        azure.translate.return_value = 'some configured azure environment'
        self._translator.add_translator('azure', azure)

        translation = self._translator.translate({'job_deployment_env': 'gcp'})
        self.assertEqual('gcp environment with configured data', translation)
    
    def test_raises_error_when_invalid_environment_requested(self):
        gcp = Mock()
        gcp.translate.return_value = 'gcp environment with configured data'
        self._translator.add_translator('gcp', gcp)

        with self.assertRaises(ValueError) as error_context:
            self._translator.translate({'job_deployment_env': 'potato'})

        self.assertIn('Got invalid deployment environment `potato`', error_context.exception.args)        
