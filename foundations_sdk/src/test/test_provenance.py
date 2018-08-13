"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations.provenance import Provenance


class TestProvenance(unittest.TestCase):
    
    class MockArchive(object):
        
        def __init__(self):
            self.job_source_bundle = None
            self.environment = {}
            self.config = {}
            # self.tags = []
            self.random_state = None
            self.module_versions = {}
            self.pip_freeze = None
            self.stage_hierarchy = None
            self.python_version = None
            self.job_archive_stuff = None
            self.other_stuff = None
            self.archive_provenance_store = None
            self.stuff = None
        
        def append_job_source(self, job_source_bundle):
            pass
        
        def append_provenance(self, archive_provenance):
            return {'version': 10}
        
        def job_archive(self):
            return 'hello'
        
        def job_source_bundle(self):
            self.job_archive_stuff = 'hana'
        
        def archive_provenance(self):
            return {
                "hello": "goodbye"
            }
        
        def fetch_provenance(self):
            return None


    # Test fill

    def setUp(self):
        from foundations.config_manager import ConfigManager
        self.config_manager = ConfigManager()

    def test_fill_python_has_correct_values(self):
        import sys
        provenance = Provenance()

        python_version = {
            "major": sys.version_info.major,
            "minor": sys.version_info.minor,
            "micro": sys.version_info.micro,
            "releaselevel": sys.version_info.releaselevel,
            "serial": sys.version_info.serial,
        }

        provenance.fill_python_version()
        self.assertEqual(provenance.python_version, python_version )
    
    def test_random_state_has_correct_value(self):
        import random
        provenance = Provenance()

        old_state = random.getstate()
        expected_state = (3, (0,) * 625, None)
        random.setstate(expected_state)
        provenance.fill_random_state()

        random.setstate(old_state)

        self.assertEqual(expected_state, provenance.random_state)
    
    def test_fill_environment_has_correct_value(self):
        import os
        provenance = Provenance()

        provenance_env_items = os.environ.items()
        provenance_env = {}
        for key, value in provenance_env_items:
            provenance_env[key] = value
            
        provenance.fill_environment()
        self.assertEqual(provenance.environment, provenance_env)

    
    def test_fill_config_with_correct_value_from_config_manager(self):
        provenance = Provenance()
        self.config_manager['other_world'] = 'aliens'
        config_return = {'other_world': 'aliens'}

        provenance.fill_config(self.config_manager)
        self.assertEqual(provenance.config, config_return)
    
    def test_fill_config_with_correct_value_from_config_manager_with_multiple_keys(self):
        provenance = Provenance()
        self.config_manager['other'] = 'value'
        self.config_manager['next'] = 'one'
        config_return = {'other': 'value', 'next': 'one'}

        provenance.fill_config(self.config_manager)
        self.assertEqual(provenance.config, config_return)
    
    def test_fill_config_with_correct_value_from_config_manager_with_empty_config(self):
        provenance = Provenance()
        config_return = {}

        provenance.fill_config(self.config_manager)
        self.assertEqual(provenance.config, config_return)


    def test_fill_pip_modules_module_versions(self):
        provenance = Provenance()

        self.assertEqual({}, provenance.module_versions)
        provenance.fill_pip_modules()
        self.assertNotEqual({}, provenance.module_versions)

    def test_fill_pip_modules_with_freeze(self):
        provenance = Provenance()

        self.assertEqual(None, provenance.pip_freeze)
        provenance.fill_pip_modules()
        self.assertNotEqual({}, provenance.pip_freeze)

    
    def test_fill_all(self):
        provenance = Provenance()
        self.assertEqual(None, provenance.python_version)
        self.assertEqual(None, provenance.random_state)
        self.assertEqual({}, provenance.environment)
        self.assertEqual({}, provenance.config)
        self.assertEqual({}, provenance.environment)
        self.assertEqual({}, provenance.module_versions)
        self.assertEqual(None, provenance.pip_freeze)
        provenance.fill_all(self.config_manager)
        self.assertNotEqual(None, provenance.python_version)
        self.assertNotEqual(None, provenance.random_state)
        self.assertNotEqual({}, provenance.environment)
        self.assertNotEqual({}, provenance.environment)
        self.assertNotEqual({}, provenance.module_versions)
        self.assertNotEqual(None, provenance.pip_freeze)
        

    # Test load

    def test_load_provenance_from_archive_with_empty_archive(self):
        provenance = Provenance()
        mock_archive = self.MockArchive()

        provenance.load_provenance_from_archive(mock_archive)
        self.assertEqual(provenance.environment, {})
        self.assertEqual(provenance.config, {})
        self.assertEqual(provenance.tags, [])
        self.assertEqual(provenance.random_state, None)
        self.assertEqual(provenance.module_versions, {})
        self.assertEqual(provenance.pip_freeze, None)
        self.assertEqual(provenance.python_version, None)
        self.assertEqual(provenance.stage_hierarchy.entries, {})
    
    def test_load_provenance_from_archive_with_specific_value_persists(self):
        provenance = Provenance()
        mock_archive = self.MockArchive()

        provenance.environment = {'python': 2}
        provenance.config = {'log_level': 'DEBUG'}
        provenance.tags = ['run_one']
        provenance.random_state = 'this is a random state'
        provenance.module_versions = {'pandas': 0.2}
        provenance.pip_freeze = 'pandas==0.2'
        provenance.python_version = {'major': 2}
        provenance.stage_hierarchy.entries = {'fake_one': 'fake_data'}

        provenance.load_provenance_from_archive(mock_archive)
        self.assertEqual(provenance.environment, {'python': 2})
        self.assertEqual(provenance.config, {'log_level': 'DEBUG'})
        self.assertEqual(provenance.tags, ['run_one'])
        self.assertEqual(provenance.random_state, 'this is a random state')
        self.assertEqual(provenance.module_versions, {'pandas': 0.2})
        self.assertEqual(provenance.pip_freeze, 'pandas==0.2')
        self.assertEqual(provenance.python_version, {'major': 2})
        self.assertEqual(provenance.stage_hierarchy.entries, {'fake_one': 'fake_data'})
        
        
    
    # Test save

    # def test_save_to_archive_job_source_none(self):
    #     provenance = Provenance()
    #     instance_of_mock = self.MockArchive()
        
    #     provenance.save_to_archive(instance_of_mock)
    #     self.assertEqual(None, provenance.job_source_bundle)
    
    # def test_save_to_archive_with_job_source(self):
    #     provenance = Provenance()
    #     instance_of_mock = self.MockArchive()

    #     instance_of_mock.append_provenance('foo')
    #     expected_result = 'hello'
    #     self.assertEqual(expected_result, provenance.tags)

    #     provenance.save_to_archive(instance_of_mock)
    #     expected_result = 'hello'
    #     self.assertEqual(expected_result, instance_of_mock.stuff)




