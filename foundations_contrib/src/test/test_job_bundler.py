"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock, call, patch

from foundations_contrib.job_bundler import JobBundler
from foundations_contrib.obfuscator import Obfuscator
from foundations_contrib.module_obfuscation_controller import ModuleObfuscationController
from foundations_contrib.resources_obfuscation_controller import ResourcesObfuscationController
from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers import let, let_mock, set_up, let_patch_mock


class TestJobBundler(Spec):

    mock_os_remove = let_patch_mock('os.remove')
    mock_tarfile_open = let_patch_mock('tarfile.open')
    mock_builtins_open = let_patch_mock('builtins.open')
    mock_yaml_dump = let_patch_mock('yaml.dump')
    mock_glob_glob = let_patch_mock('glob.glob')
    mock_os_chdir = let_patch_mock('os.chdir')
    mock_simple_temp_file_class = let_patch_mock('foundations_contrib.simple_tempfile.SimpleTempfile')

    @let
    def _default_config(self):
        return {
            'obfuscate_foundations': False,
            'deployment_implementation': {
                'deployment_type': 'something'
            }
        }

    @staticmethod
    def _return_generator(input):
        for item in input:
            yield item

    class MockContextManager(Mock):

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            return self

    class MockObfuscationContextManager(object):

        def __init__(self):
            self.entered = False
            self.exited = False

        def __enter__(self):
            self.entered = True
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.exited = True
            return self

        def get_resources(self):
            pass

        def get_foundations_modules(self):
            pass

    class MockJobSourceBundle(Mock):

        def __init__(self, archive_name):
            super().__init__()
            self._archive_name = archive_name

        def job_archive(self):
            return self._archive_name
    
        def bundle(self):
            pass
    
        def cleanup(self):
            pass

    class MockSimpleTempfile(MockContextManager):

        def __init__(self, temp_file_name):
            super().__init__()
            self.name = temp_file_name


    class MockJob(Mock):

        def serialize(self):
            pass

    def test_job_name_method_returns_job_name(self):
       job_bundler = JobBundler('fake_name', {}, None, None)
       self.assertEqual(job_bundler.job_name(), 'fake_name')

    def test_job_archive_name_method_returns_job_archive_name(self):
       job_bundler = JobBundler('fake_name', {}, None, None)
       self.assertEqual(job_bundler.job_archive_name(), 'fake_name.tgz')

    def test_job_archive_method_returns_job_archive(self):
       job_bundler = JobBundler('fake_name', {}, None, None)
       self.assertEqual(job_bundler.job_archive(), '../fake_name.tgz')

    def test_cleanup_removes_correct_files(self):
        job_bundler = JobBundler('fake_name', {}, None, None)
        job_bundler.cleanup()
        remove_archive = call('../fake_name.tgz')
        remove_bin = call('fake_name.bin')
        remove_config = call('fake_name.config.yaml')
        self.mock_os_remove.assert_has_calls([remove_archive, remove_bin, remove_config])

    def test_unbundle_opens_correct_file(self):
        job_bundler = JobBundler('fake_name', {}, None, None)
        job_bundler.unbundle()
        self.mock_tarfile_open.assert_called_with('../fake_name.tgz', 'r:gz')

    def test_unbundle_extracts_from_tarfile(self):
        return_object = self.MockContextManager()
        self.mock_tarfile_open.return_value = return_object
        job_bundler = JobBundler('fake_name', {}, None, None)
        job_bundler.unbundle()
        return_object.extractall.assert_called()

    def test_save_job_opens_file(self):
        mock_job = self._create_mock_job()
        job_bundler = JobBundler('fake_name', {}, mock_job, None)
        job_bundler._save_job()
        self.mock_builtins_open.assert_called_with('fake_name.bin', 'w+b')

    def test_save_job_writes_to_file(self):
        mock_job = self._create_mock_job()
        return_object = self.MockContextManager()
        self.mock_builtins_open.return_value = return_object
        job_bundler = JobBundler('fake_name', {}, mock_job, None)
        job_bundler._save_job()
        return_object.write.assert_called_with('something')

    def test_save_config_opens_file(self):
        mock_job = self._create_mock_job()
        job_bundler = JobBundler('fake_name', {}, mock_job, None)
        job_bundler._save_config()
        self.mock_builtins_open.assert_called_with('fake_name.config.yaml', 'w+')

    def test_save_config_dumps_to_file(self):
        mock_job = self._create_mock_job()
        return_object = self.MockContextManager()
        self.mock_builtins_open.return_value = return_object
        job_bundler = JobBundler('fake_name', {}, mock_job, None)
        job_bundler._save_config()
        self.mock_yaml_dump.assert_called_with({'job_name': 'fake_name'}, return_object)

    def test_bundle_job_opens_file(self):
        mock_job_source_bundle = self.MockJobSourceBundle('fake_source_archive_name')

        job_bundler = JobBundler('fake_name', self._default_config, None, mock_job_source_bundle)
        job_bundler._bundle_job()
        self.mock_tarfile_open.assert_called_with('../fake_name.tgz', 'w:gz')

    def test_bundle_job_adds_archive_and_binary_to_tarball(self):
        mock_job_source_bundle, mock_tar = self._setup_archive_and_tar()
        job_bundler = JobBundler('fake_name', {}, None, mock_job_source_bundle)
        job_bundler._bundle_job()
        add_archive_call = call('fake_source_archive_name', arcname='fake_name/job.tgz')
        add_binary_call = call('fake_name.bin', arcname='fake_name/fake_name.bin')
        mock_tar.add.assert_has_calls([add_archive_call, add_binary_call], any_order=True)

    def test_bundle_job_adds_config_files(self):
        mock_job_source_bundle, mock_tar = self._setup_archive_and_tar()
        self.mock_glob_glob.return_value = ['fake_config_filename.config.yaml']
        job_bundler = JobBundler('fake_name', {}, None, mock_job_source_bundle)
        job_bundler._bundle_job()
        add_config_call = call('fake_config_filename.config.yaml', arcname='fake_name/fake_config_filename.config.yaml')
        mock_tar.add.assert_has_calls([add_config_call])


    @patch.object(ModuleObfuscationController, 'get_foundations_modules')
    def test_bundle_calls_module_obfuscation_controller(self, mock_get_foundations_modules):
        config = {}
        mock_job_source_bundle, _ = self._setup_archive_and_tar()
        mock_job = self.MockJob()
        job_bundler = JobBundler('fake_name', config, mock_job, mock_job_source_bundle)
        job_bundler.bundle()

        mock_get_foundations_modules.assert_called()

    @patch.object(ModuleObfuscationController, 'get_foundations_modules')
    def test_bundle_add_module_directory_to_tar(self, mock_get_foundations_modules):
        mock_job_source_bundle, mock_tar = self._setup_archive_and_tar()
        mock_get_foundations_modules.return_value = self._return_generator([('fake_module_name', 'fake_module_directory')])

        job_bundler = JobBundler('fake_name', {}, self.MockJob(), mock_job_source_bundle)
        job_bundler.bundle()

        mock_tar.add.assert_any_call('fake_module_directory', arcname='fake_name/fake_module_name')
    
    @patch.object(ModuleObfuscationController, 'get_foundations_modules')
    def test_bundle_add_module_directory_to_tar_different_name(self, mock_get_foundations_modules):
        mock_job_source_bundle, mock_tar = self._setup_archive_and_tar()
        mock_get_foundations_modules.return_value = self._return_generator([('real_module_name', 'real_module_directory')])

        job_bundler = JobBundler('real_name', {}, self.MockJob(), mock_job_source_bundle)
        job_bundler.bundle()

        mock_tar.add.assert_any_call('real_module_directory', arcname='real_name/real_module_name')

    @patch.object(ModuleObfuscationController, 'get_foundations_modules')
    def test_bundle_add_module_directory_to_tar_multiple_modules(self, mock_get_foundations_modules):
        mock_job_source_bundle, mock_tar = self._setup_archive_and_tar()
        mock_get_foundations_modules.return_value = self._return_generator([('real_module_name', 'real_module_directory'), ('totally_fake_module_name', 'lol_directory')])

        job_bundler = JobBundler('real_name', {}, self.MockJob(), mock_job_source_bundle)
        job_bundler.bundle()

        mock_tar.add.assert_any_call('real_module_directory', arcname='real_name/real_module_name')
        mock_tar.add.assert_any_call('lol_directory', arcname='real_name/totally_fake_module_name')

    @patch('foundations_contrib.module_obfuscation_controller.ModuleObfuscationController')
    def test_bundle_job_adds_script_environment(self, mock_module_obfuscation_controller):
        import foundations_contrib

        mock_job_source_bundle, mock_tar = self._setup_archive_and_tar()

        self.mock_simple_temp_file_class.return_value = self.MockSimpleTempfile('fake_temp_file_name')
        with patch.object(foundations_contrib.job_bundling.script_environment.ScriptEnvironment, 'write_environment'):
            fake_config = {'run_script_environment': ''}
            job_bundler = JobBundler('fake_name', fake_config, self.MockJob(), mock_job_source_bundle)
            job_bundler.bundle()

        mock_tar.add.assert_has_calls([call('fake_temp_file_name', arcname='fake_name/run.env')])

    @patch.object(ResourcesObfuscationController, '__enter__')
    def test_bundle_enters_resource_obfuscation_controller_context_manager(self, mock_resources_obfuscation_controller_enter):

        mock_job_source_bundle, mock_tar = self._setup_archive_and_tar()

        job_bundler = JobBundler('fake_name', self._default_config, self.MockJob(), mock_job_source_bundle)
        job_bundler.bundle()

        mock_resources_obfuscation_controller_enter.assert_called()


    @patch.object(ResourcesObfuscationController, '__exit__')
    def test_bundle_exits_resource_obfuscation_controller_context_manager(self, mock_resources_obfuscation_controller_exit):

        mock_job_source_bundle, mock_tar = self._setup_archive_and_tar()

        job_bundler = JobBundler('fake_name', self._default_config, self.MockJob(), mock_job_source_bundle)
        job_bundler.bundle()

        mock_resources_obfuscation_controller_exit.assert_called()
        
    @patch.object(ResourcesObfuscationController, 'get_resources')
    def test_bundle_calls_resource_obfuscation_controller(self, mock_resources_obfuscation_controller_get_resources):
        mock_job_source_bundle, mock_tar = self._setup_archive_and_tar()

        job_bundler = JobBundler('fake_name', self._default_config, self.MockJob(), mock_job_source_bundle)
        job_bundler.bundle()

        mock_resources_obfuscation_controller_get_resources.assert_called()

    @patch.object(ResourcesObfuscationController, 'get_resources')
    def test_bundle_adds_resources_directory(self, mock_resources_obfuscation_controller_get_resources):
        mock_resources_obfuscation_controller_get_resources.return_value = '/directory/path/resources'
        mock_job_source_bundle, mock_tar = self._setup_archive_and_tar()

        job_bundler = JobBundler('fake_name', self._default_config, self.MockJob(), mock_job_source_bundle)
        job_bundler.bundle()

        self.mock_os_chdir.assert_has_calls([call('/directory/path/resources')])
        mock_tar.add.assert_has_calls([call('.', arcname='fake_name')])


    @patch.object(ModuleObfuscationController, '__enter__')
    def test_bundle_enters_module_obfuscation_controller_context_manager(self, mock_module_obfuscation_controller_enter):

        mock_job_source_bundle, mock_tar = self._setup_archive_and_tar()

        job_bundler = JobBundler('fake_name', self._default_config, self.MockJob(), mock_job_source_bundle)
        job_bundler.bundle()

        mock_module_obfuscation_controller_enter.assert_called()
    

    @patch.object(ModuleObfuscationController, '__exit__')
    def test_bundle_exits_module_obfuscation_controller_context_manager(self, mock_module_obfuscation_controller_exit):

        mock_job_source_bundle, mock_tar = self._setup_archive_and_tar()

        job_bundler = JobBundler('fake_name', self._default_config, self.MockJob(), mock_job_source_bundle)
        job_bundler.bundle()

        mock_module_obfuscation_controller_exit.assert_called()
        

    def _setup_archive_and_tar(self):
        mock_job_source_bundle = self.MockJobSourceBundle('fake_source_archive_name')
        mock_tar = self.MockContextManager()
        self.mock_tarfile_open.return_value = mock_tar

        return mock_job_source_bundle, mock_tar

    def _create_mock_job(self):
        mock_job = Mock()
        mock_job.serialize = lambda: 'something'
        return mock_job
