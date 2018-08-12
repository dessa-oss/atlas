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
            self.environment = None
            self.config = None
            self.tags = None
            self.random_state = None
            self.module_versions = None
            self.pip_freeze = None
            self.stage_hierarchy = None
            self.python_version = None
            self.job_archive = None
            self.other_stuff = None
        
        def append_job_source(self, job_source_bundle):
            pass
        
        def append_provenance(self, archiver_provenance):
            pass
        
        def job_archive(self):
            return 'hello'
        
        def job_source_bundle(self):
            self.job_archive = 'hana'
        
        def _archive_provenance(self):
            return {
                "hello": "goodbye"
            }

    


    # Test fill

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

        random_state = random.getstate()
        provenance.fill_random_state()

        self.assertEqual(provenance.random_state, random_state)
    
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
        from foundations.global_state import config_manager
        provenance = Provenance()
        config_manager.config()['other_world'] = 'aliens'
        config_return = config_manager.config()

        provenance.fill_config()
        self.assertEqual(provenance.config, config_return)
    
    def test_fill_config_with_correct_value_from_config_manager_with_multiple_keys(self):
        from foundations.global_state import config_manager
        provenance = Provenance()
        config_manager.config()['other_world'] = 'aliens'
        config_return = config_manager.config()

        provenance.fill_config()
        self.assertEqual(provenance.config, config_return)
    
    def test_fill_config_with_correct_value_from_config_manager_with_empty_config(self):
        from foundations.global_state import config_manager
        provenance = Provenance()
        config_return = config_manager.config()

        provenance.fill_config()
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
        provenance.fill_all()
        self.assertNotEqual(None, provenance.python_version)
        self.assertNotEqual(None, provenance.random_state)
        self.assertNotEqual({}, provenance.environment)
        self.assertNotEqual({}, provenance.environment)
        self.assertNotEqual({}, provenance.module_versions)
        self.assertNotEqual(None, provenance.pip_freeze)
        

    # Test load

    def test_load_provenance_from_archive_with_empty_archive(self):
        provenance = Provenance()
        archive_provenance = False

        provenance.load_provenance_from_archive(archive_provenance)
        self.assertEqual(provenance.environment, {})
    
    # Test save

    def test_save_to_archive_job_source_none(self):
        archive = Provenance()
        instance_of_mock = self.MockArchive()
        archive.save_to_archive(instance_of_mock)
        self.assertEqual(None, archive.job_source_bundle)
    
    # def test_save_to_archive(self):
    #     archive = Provenance()
    #     instance_of_mock = self.MockArchive()
    #     archive.save_to_archive(instance_of_mock)
    #     self.assertEqual('hana', instance_of_mock.job_source_bundle)







    # def test_save_archive_if_job_source_exists(self):
    
    #     provenance = Provenance()

    #     archive_provenance = {}
    #     class Archive(self):
    #         def __init__(self):
    #             self.provenance = None

    #         def append_provenance(self, provenance):
    #             self.archive_provenance = provenance

    #     mock_instance_archive_provenance = ArchiveProvenance()

    #     mock_value = {
    #         "environment": self.environment,
    #         "config": self.config,
    #         "tags": self.tags,
    #         "random_state": self.random_state,
    #         "module_versions": self.module_versions,
    #         "pip_freeze": self.pip_freeze,
    #         "stage_hierarchy": self.stage_hierarchy,
    #         "python_version": self.python_version
    #     }

    #     print( , mock_instance_archive_provenance)