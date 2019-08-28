"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations_spec.helpers import set_up, tear_down
from foundations_spec.helpers.spec import Spec
from foundations_contrib.local_shell_job_deployment import LocalShellJobDeployment
from foundations import config_manager

class TestLocalObfuscateJobs(Spec):

    def setUp(self):
        from acceptance.cleanup import cleanup
        cleanup()


    def test_job_does_not_obfuscates_source_code_when_local_and_obfuscate_true(self):
        import foundations        
        import os
        import time
        import glob
        from multiprocessing import Process, Value

        def run_foundations_func(bundling):
            from acceptance.fixtures.stages import add_two_numbers

            add_two_numbers = foundations.create_stage(add_two_numbers)
            add_two_numbers_deployment_object = add_two_numbers(3, 5).run()
            add_two_numbers_deployment_object.wait_for_deployment_to_complete()
            bundling.value = 0

        def monitor_processes_func(bundling, pyarmor_run):
            cmdlines = []
            while bundling.value:
                for cmdline_file_path in glob.glob('/proc/*/cmdline'):
                    # Trying to fight the filesystem race condition as much as possible at the expense of RAM
                    try:
                        with open(cmdline_file_path, 'rb') as cmdline_file:
                            cmdlines.append(cmdline_file.readline())
                    except (FileNotFoundError, ProcessLookupError):
                        pass
            # Now calmly search in the data dumped to RAM for our target
            for cmdline in cmdlines:
                if cmdline:
                    pyarmor_run.value += cmdline.decode().find('pyarmor\0obfuscate') + 1


        config_manager['obfuscate_foundations'] = True

        config_manager['deployment_implementation'] = {
            'deployment_type': LocalShellJobDeployment
        }

        pyarmor_run = Value('i', 0)
        bundling = Value('i', 1)

        monitor_processes = Process(target=monitor_processes_func, args=(bundling, pyarmor_run))
        run_foundations = Process(target=run_foundations_func, args=(bundling,))
        monitor_processes.start()
        time.sleep(0.001)
        run_foundations.start()
        run_foundations.join()
        monitor_processes.join()

        self.assertTrue(pyarmor_run.value == 0)


    def _check_source_code_obfuscated(self, job_id):
        import os
        import tarfile
        import shutil
        from foundations_internal.change_directory import ChangeDirectory

        job_archive_location = os.path.join(config_manager['archive_listing_implementation']['constructor_arguments'][0], job_id, 'job_source')
        with ChangeDirectory(job_archive_location):

            job_tar_name = '{}.tgz'.format(job_id)

            foundations_init_file_location = os.path.join(job_id, 'foundations', '__init__.py')

            with tarfile.open(job_tar_name, "r:gz") as tar:
                tar.extract(foundations_init_file_location)
            
            with open(foundations_init_file_location, 'rb') as init_file:
                file_head = init_file.readline()[0:11]
        shutil.rmtree(os.path.join(job_archive_location, job_id))
        
        return file_head == b'__pyarmor__'