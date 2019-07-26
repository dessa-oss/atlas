"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_internal.provenance import Provenance
from foundations_spec import *

class TestProvenance(Spec):

    class MockArchive(object):

        def __init__(self):
            self.job_source_bundle = None
            self.environment = {}
            self.config = {}
            self.tags = []
            self.random_state = None
            self.module_versions = {}
            self.pip_freeze = None
            self.stage_hierarchy = None
            self.python_version = None
            self.job_archive_stuff = None
            self.other_stuff = None
            self.archive_provenance = None

        def append_job_source(self, job_source_bundle):
            self.job_source_bundle = job_source_bundle

        def append_provenance(self, archive_provenance):
            self.archive_provenance = archive_provenance

        def fetch_provenance(self):
            return self.archive_provenance

    class MockArchiveWithJobArchive(object):

        def job_archive(self):
            return 'space'

    @let
    def config_manager(self):
        from foundations.config_manager import ConfigManager
        return ConfigManager()

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
        self.assertEqual(provenance.python_version, python_version)

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

        provenance.fill_config(self.config_manager)
        self.assertEqual(provenance.config['other_world'], 'aliens')

    def test_fill_config_with_correct_value_from_config_manager_with_multiple_keys(self):
        provenance = Provenance()
        self.config_manager['other'] = 'value'
        self.config_manager['next'] = 'one'

        provenance.fill_config(self.config_manager)
        self.assertEqual(provenance.config['other'], 'value')
        self.assertEqual(provenance.config['next'], 'one')

    def test_fill_config_with_correct_value_from_config_manager_with_empty_config(self):
        self.patch('os.environ', {})

        provenance = Provenance()
        config_return = {'run_script_environment': {}}

        provenance.fill_config(self.config_manager)
        self.assertDictEqual(provenance.config, config_return)

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
        self.assertNotEqual({}, provenance.module_versions)
        self.assertNotEqual(None, provenance.pip_freeze)

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
        self.assertEqual(provenance.job_run_data, {})
        self.assertEqual(provenance.project_name, 'default')
        self.assertEqual(provenance.user_name, 'trial')
        self.assertEqual(provenance.annotations, {})

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
        provenance.job_run_data = {'layers': 99, 'neurons_per_layer': 9999}
        provenance.project_name = 'my wonderful project'
        provenance.user_name = 'Alan Turing'
        provenance.annotations = {'model': 'mlp', 'layer': 'all of them'}
        provenance.save_to_archive(mock_archive)

        provenance_two = Provenance()
        provenance_two.load_provenance_from_archive(mock_archive)

        self.assertEqual(provenance_two.environment, {'python': 2})
        self.assertEqual(provenance_two.config, {'log_level': 'DEBUG'})
        self.assertEqual(provenance_two.tags, ['run_one'])
        self.assertEqual(provenance_two.random_state, 'this is a random state')
        self.assertEqual(provenance_two.module_versions, {'pandas': 0.2})
        self.assertEqual(provenance_two.pip_freeze, 'pandas==0.2')
        self.assertEqual(provenance_two.python_version, {'major': 2})
        self.assertEqual(provenance_two.stage_hierarchy.entries,
                         {'fake_one': 'fake_data'})
        self.assertEqual(provenance_two.job_run_data, {
                         'layers': 99, 'neurons_per_layer': 9999})
        self.assertEqual(provenance_two.project_name, 'my wonderful project')
        self.assertEqual(provenance_two.user_name, 'Alan Turing')
        self.assertEqual(provenance_two.annotations, {'model': 'mlp', 'layer': 'all of them'})

    def test_save_to_archive_with_no_job_source(self):
        provenance = Provenance()
        mock_archive = self.MockArchive()

        provenance.save_to_archive(mock_archive)
        self.assertDictContainsSubset({'config': {},
                                       'environment': {},
                                       'module_versions': {},
                                       'pip_freeze': None,
                                       'python_version': None,
                                       'random_state': None,
                                       'tags': [],
                                       'job_run_data': {},
                                       'project_name': 'default',
                                       'user_name': 'trial',
                                       }, mock_archive.archive_provenance)
        self.assertEqual(
            {}, mock_archive.archive_provenance['stage_hierarchy'].entries)

    def test_save_to_archive_with_no_job_source_with_values(self):
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
        provenance.job_run_data = {'layers': 99, 'neurons_per_layer': 9999}
        provenance.project_name = 'a different project'
        provenance.user_name = 'Richard Hamming'
        provenance.save_to_archive(mock_archive)

        self.assertDictContainsSubset({'config': {'log_level': 'DEBUG'},
                                       'environment': {'python': 2},
                                       'module_versions': {'pandas': 0.2},
                                       'pip_freeze': 'pandas==0.2',
                                       'python_version': {'major': 2},
                                       'random_state': 'this is a random state',
                                       'tags': ['run_one'],
                                       'job_run_data': {'layers': 99, 'neurons_per_layer': 9999},
                                       'project_name': 'a different project',
                                       'user_name': 'Richard Hamming'
                                       }, mock_archive.archive_provenance)
        self.assertEqual({'fake_one': 'fake_data'},
                         mock_archive.archive_provenance['stage_hierarchy'].entries)

    def test_save_to_archive_with_job_source(self):
        provenance = Provenance()
        mock_archive = self.MockArchive()

        provenance.job_source_bundle = self.MockArchiveWithJobArchive()
        provenance.save_to_archive(mock_archive)
        self.assertEqual('space', mock_archive.job_source_bundle)

    def test_load_artifact_from_archive(self):
        provenance = Provenance()
        mock_archive = self.MockArchive()

        provenance.load_artifact_from_archive(mock_archive)

    def test_load_miscellaneous_from_archive(self):
        provenance = Provenance()
        mock_archive = self.MockArchive()

        provenance.load_miscellaneous_from_archive(mock_archive)

    def test_load_stage_log_from_archive(self):
        provenance = Provenance()
        mock_archive = self.MockArchive()

        provenance.load_stage_log_from_archive(mock_archive)

    def test_load_persisted_data_from_archive(self):
        provenance = Provenance()
        mock_archive = self.MockArchive()

        provenance.load_persisted_data_from_archive(mock_archive)

    def test_provenance_default_project_name(self):
        provenance = Provenance()
        self.assertEqual(provenance.project_name, "default")

    def test_provenance_default_user_name(self):
        provenance = Provenance()
        self.assertEqual(provenance.user_name, "trial")
